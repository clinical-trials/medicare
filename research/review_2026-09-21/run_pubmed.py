"""Archive an executed, pre-PRESS PubMed search without making eligibility decisions.

Network requests use NCBI E-utilities. Raw responses are immutable after capture.
Date partitions overcome ESearch's 9,999-ID limit, with PMID-set reconciliation.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARCHIVE = HERE / "pubmed"
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def request(endpoint, params, name):
    path = ARCHIVE / "raw" / name
    meta_path = path.with_suffix(path.suffix + ".request.json")
    if path.exists():
        stored = path.read_bytes()
        return gzip.decompress(stored) if path.suffix == ".gz" else stored
    params = {"db": "pubmed", "tool": "MedicareEvidenceReview", **params}
    url = BASE + endpoint + "?" + urllib.parse.urlencode(params)
    use_post = endpoint == "efetch.fcgi" and len(url) > 3500
    req = urllib.request.Request(BASE + endpoint, data=urllib.parse.urlencode(params).encode()) if use_post else url
    for attempt in range(4):
        try:
            started = now()
            with urllib.request.urlopen(req, timeout=60) as response:
                body = response.read()
            # Validate before storing so an HTML error never masquerades as an export.
            if endpoint == "esearch.fcgi":
                parsed = json.loads(body)
                if "esearchresult" not in parsed or "ERROR" in parsed:
                    raise ValueError(body[:500])
            else:
                ET.fromstring(body)
            path.parent.mkdir(parents=True, exist_ok=True)
            stored = gzip.compress(body, mtime=0) if path.suffix == ".gz" else body
            path.write_bytes(stored)
            save_json(meta_path, {"requested_at_utc": started, "completed_at_utc": now(),
                "url": BASE + endpoint if use_post else url, "method": "POST" if use_post else "GET",
                "params": params, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                "storage": "lossless gzip" if path.suffix == ".gz" else "original bytes",
                "stored_sha256": hashlib.sha256(stored).hexdigest()})
            time.sleep(0.38)
            return body
        except Exception as exc:
            if attempt == 3:
                raise
            print(f"retry {name}: {exc}", flush=True)
            time.sleep(2 ** (attempt + 1))

def search(query, name):
    return json.loads(request("esearch.fcgi", {"term": query, "retmode": "json", "retmax": 9999}, name + ".json"))["esearchresult"]

def query_definitions():
    path = ARCHIVE / "queries.json"
    if path.exists():
        return json.loads(path.read_text())
    draft = (ROOT / "research/submission/search_strategy_draft.md").read_text()
    core, supplement = re.findall(r"```text\n(.*?)\n```", draft, re.S)[:2]
    sex = '(sex[tiab] OR gender[tiab] OR women[tiab] OR men[tiab] OR female*[tiab] OR male*[tiab])'
    valuation = '("relative value"[tiab] OR RVU[tiab] OR RVUs[tiab] OR "physician fee schedule"[tiab])'
    result = {"created_at_utc": now(), "protocol": "Draft v0.1 dated 2026-09-16; execution before PRESS review",
        "searcher": "Codex AI assistant", "peer_review": "Not performed", "queries": [
        {"id": "PM-CORE-20260921", "purpose": "Unrestricted core from draft", "query": core},
        {"id": "PM-SUPP-20260921", "purpose": "Sex/gender valuation/cost supplementary query from draft", "query": supplement},
        {"id": "PM-PRIORITY-20260921", "purpose": "Title/abstract export priority subset; NOT an exclusion filter", "query": f"(({core}) AND {sex}) OR ({sex} AND {valuation})"}
    ]}
    save_json(path, result)
    return result

def collect(query, qid, low=1000, high=3000):
    # The top query itself has no publication-date filter. Partitions are technical only.
    result = search(query, qid + "_total")
    expected = int(result["count"])
    if expected <= 9999:
        return set(result["idlist"]), expected, [qid + "_total.json"]
    files = [qid + "_total.json"]
    def part(a, b):
        name = f"{qid}_{a}_{b}"
        subset = search(f'({query}) AND ("{a}/01/01"[Date - Publication] : "{b}/12/31"[Date - Publication])', name)
        files.append(name + ".json")
        if int(subset["count"]) <= 9999:
            return set(subset["idlist"])
        if a == b:
            raise ValueError(f"Single year {a} exceeds ESearch limit; needs finer partition")
        middle = (a + b) // 2
        return part(a, middle) | part(middle + 1, b)
    ids = part(low, high)
    if len(ids) != expected:
        # Identify records without a matching publication date rather than silently lose them.
        remainder = search(f'({query}) NOT ("{low}/01/01"[Date - Publication] : "{high}/12/31"[Date - Publication])', qid + "_undated")
        files.append(qid + "_undated.json")
        ids |= set(remainder["idlist"])
    if len(ids) != expected:
        raise ValueError(f"Reconciliation failed {qid}: root {expected}, unique IDs {len(ids)}")
    return ids, expected, files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["ids", "repair", "metadata", "all_metadata"], required=True)
    args = parser.parse_args()
    defs = query_definitions()
    manifest_path = ARCHIVE / "manifest.json"
    if args.stage == "ids":
        runs = []
        for q in defs["queries"]:
            ids, count, files = collect(q["query"], q["id"])
            ordered = sorted(ids, key=int)
            p = ARCHIVE / (q["id"] + ".pmids.txt")
            p.write_text("\n".join(ordered) + "\n")
            runs.append({**q, "retrieved_count": count, "exported_unique_pmids": len(ids), "raw_search_files": files,
                "id_export": p.name, "id_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                "translation": json.loads((ARCHIVE / "raw" / files[0]).read_text())["esearchresult"].get("querytranslation"),
                "warnings": json.loads((ARCHIVE / "raw" / files[0]).read_text())["esearchresult"].get("warninglist", {})})
            save_json(manifest_path, {"updated_at_utc": now(), "status": "Executed pre-PRESS search; not completed review selection", "runs": runs})
            print(f"{q['id']}: {count} results; all {len(ids)} PMIDs archived", flush=True)
        union = set()
        for run in runs[:2]:
            union.update((ARCHIVE / run["id_export"]).read_text().splitlines())
        manifest = json.loads(manifest_path.read_text())
        manifest["core_supplement_union"] = len(union)
        manifest["duplicate_query_hits"] = sum(r["retrieved_count"] for r in runs[:2]) - len(union)
        (ARCHIVE / "core_supplement_unique_pmids.txt").write_text("\n".join(sorted(union, key=int)) + "\n")
        save_json(manifest_path, manifest)
    elif args.stage == "repair":
        manifest = json.loads(manifest_path.read_text())
        repairs = []
        for q in [defs["queries"][0], defs["queries"][2]]:
            corrected = q["query"].replace('"Drug Formularies"[Mesh]', '"Formularies as Topic"[Mesh]')
            qid = q["id"] + "-R1"
            total = search(corrected, qid + "_total")
            added = search(f'({corrected}) NOT ({q["query"]})', qid + "_added")
            removed = search(f'({q["query"]}) NOT ({corrected})', qid + "_removed")
            assert int(added["count"]) <= 9999 and int(removed["count"]) <= 9999
            ids = set((ARCHIVE / (q["id"] + ".pmids.txt")).read_text().splitlines())
            ids = (ids | set(added["idlist"])) - set(removed["idlist"])
            assert len(ids) == int(total["count"]), "Corrected query count does not reconcile"
            p = ARCHIVE / (qid + ".pmids.txt")
            p.write_text("\n".join(sorted(ids, key=int)) + "\n")
            repairs.append({"id": qid, "supersedes_for_current_search": q["id"], "query": corrected,
                "reason": 'ESearch reported unrecognized "Drug Formularies"[Mesh]; replaced with "Formularies as Topic"[Mesh]',
                "retrieved_count": int(total["count"]), "exported_unique_pmids": len(ids),
                "added": added["idlist"], "removed": removed["idlist"], "id_export": p.name,
                "id_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                "translation": total.get("querytranslation"), "warnings": total.get("warninglist", {}),
                "raw_search_files": [qid + s + ".json" for s in ["_total", "_added", "_removed"]]})
            print(f"{qid}: {len(ids)} IDs; added {len(added['idlist'])}, removed {len(removed['idlist'])}", flush=True)
        manifest["query_repairs"] = repairs
        union = set((ARCHIVE / repairs[0]["id_export"]).read_text().splitlines())
        supplemental = set((ARCHIVE / "PM-SUPP-20260921.pmids.txt").read_text().splitlines())
        union |= supplemental
        manifest["current_unique_records"] = len(union)
        manifest["current_duplicate_query_hits"] = repairs[0]["retrieved_count"] + len(supplemental) - len(union)
        (ARCHIVE / "current_unique_pmids.txt").write_text("\n".join(sorted(union, key=int)) + "\n")
        save_json(manifest_path, manifest)
    elif args.stage == "metadata":
        qid = "PM-PRIORITY-20260921-R1"
        ids = (ARCHIVE / (qid + ".pmids.txt")).read_text().splitlines()
        for start in range(0, len(ids), 200):
            batch = ids[start:start + 200]
            name = f"priority_metadata_{start:06}.xml"
            data = request("efetch.fcgi", {"id": ",".join(batch), "retmode": "xml"}, name)
            root = ET.fromstring(data)
            got = {e.findtext("MedlineCitation/PMID") or e.findtext("BookDocument/PMID") for e in root}
            if got != set(batch):
                raise ValueError(f"Missing/unexpected EFetch IDs at {start}: {set(batch)-got}, {got-set(batch)}")
            print(f"metadata {start + len(batch)}/{len(ids)}", flush=True)
        manifest = json.loads(manifest_path.read_text())
        manifest["metadata_export"] = {"subset_query": qid, "records": len(ids),
            "completed_at_utc": now(), "limitation": "Only priority subset has title/abstract XML; all core/supplement IDs retained. No records excluded by prioritization."}
        save_json(manifest_path, manifest)
    else:
        all_ids = set((ARCHIVE / "current_unique_pmids.txt").read_text().splitlines())
        priority = set((ARCHIVE / "PM-PRIORITY-20260921-R1.pmids.txt").read_text().splitlines())
        ids = sorted(all_ids - priority, key=int)
        for start in range(0, len(ids), 400):
            batch = ids[start:start + 400]
            name = f"remaining_metadata_{start:06}.xml.gz"
            data = request("efetch.fcgi", {"id": ",".join(batch), "retmode": "xml"}, name)
            root = ET.fromstring(data)
            got = {e.findtext("MedlineCitation/PMID") or e.findtext("BookDocument/PMID") for e in root}
            if got != set(batch):
                raise ValueError(f"Missing/unexpected EFetch IDs at {start}: {set(batch)-got}, {got-set(batch)}")
            print(f"remaining metadata {start + len(batch)}/{len(ids)}", flush=True)
        manifest = json.loads(manifest_path.read_text())
        manifest["complete_metadata_export"] = {"records": len(all_ids), "priority_records": len(priority),
            "additional_records": len(ids), "completed_at_utc": now(),
            "status": "All current unique query results have PubMed XML metadata; abstract absence retained, no screening inferred"}
        save_json(manifest_path, manifest)

if __name__ == "__main__":
    main()
