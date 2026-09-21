"""Prepare reversible PMID deduplication, machine-readable exports and calibration set.

No screening decisions or clinical eligibility decisions are made by this script.
"""
import csv
import hashlib
import gzip
import io
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARC = HERE / "pubmed"

def text(el):
    return "".join(el.itertext()).strip() if el is not None else ""

def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in fields} for row in rows)

def main():
    manifest = json.loads((ARC / "manifest.json").read_text())
    assert "metadata_export" in manifest, "Wait for complete priority metadata export"
    core = set((ARC / "PM-CORE-20260921-R1.pmids.txt").read_text().splitlines())
    supp = set((ARC / "PM-SUPP-20260921.pmids.txt").read_text().splitlines())
    union = core | supp
    assert len(union) == manifest["current_unique_records"]
    expected = set((ARC / "PM-PRIORITY-20260921-R1.pmids.txt").read_text().splitlines())
    existing = json.loads((ROOT / "research/bibliography_metadata.json").read_text())["records"]
    old = {m.get("pmid"): m for m in existing}
    complete = "complete_metadata_export" in manifest
    records = []
    paths = sorted((ARC / "raw").glob("priority_metadata_*.xml"))
    if complete:
        paths += sorted((ARC / "raw").glob("remaining_metadata_*.xml.gz"))
    for path in paths:
        data = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
        for record in ET.fromstring(data):
            pmid = record.findtext("MedlineCitation/PMID") or record.findtext("BookDocument/PMID")
            article = record.find("MedlineCitation/Article")
            is_book = article is None
            if article is None:
                article = record.find("BookDocument")
            article_title = text(article.find("ArticleTitle"))
            book_title = text(article.find("Book/BookTitle")) if is_book else ""
            document_type = ("book_chapter" if article_title else "book") if is_book else "journal_article"
            authors = []
            author_nodes = article.findall("AuthorList/Author")
            if is_book and not article_title and not author_nodes:
                # A book can have corporate authors; do not relabel its editors as authors.
                author_nodes = article.findall("Book/AuthorList[@Type='authors']/Author")
            for a in author_nodes:
                authors.append(text(a.find("CollectiveName")) or (text(a.find("LastName")) + " " + text(a.find("Initials"))).strip())
            id_path = "BookDocument/ArticleIdList/ArticleId" if is_book else "PubmedData/ArticleIdList/ArticleId"
            ids = {a.get("IdType"): text(a) for a in record.findall(id_path)}
            abstract = "\n".join((a.get("Label", "") + ": " if a.get("Label") else "") + text(a) for a in article.findall("Abstract/AbstractText"))
            date_path = "Book/PubDate" if is_book else "Journal/JournalIssue/PubDate"
            year = text(article.find(date_path + "/Year"))
            if not year:
                match = re.search(r"\d{4}", text(article.find(date_path + "/MedlineDate")))
                year = match.group() if match else text(article.find("ArticleDate/Year"))
            publication_type_path = "PublicationType" if is_book else "PublicationTypeList/PublicationType"
            records.append({"record_id": "R-" + pmid, "existing_study_id": old.get(pmid, {}).get("id", ""),
                "pmid": pmid, "title": article_title or book_title, "authors": "; ".join(authors),
                "year": int(year) if year else None, "journal": text(article.find("Journal/Title")),
                "document_type": document_type, "book_title": book_title,
                "publisher": text(article.find("Book/Publisher/PublisherName")) if is_book else "",
                "doi": ids.get("doi", ""), "pmcid": ids.get("pmc", ""), "abstract": abstract,
                "publication_types": "; ".join(text(a) for a in article.findall(publication_type_path)),
                "source_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/", "raw_xml": str(path.relative_to(ROOT)),
                "in_core": pmid in core, "in_supplement": pmid in supp,
                "status": "Awaiting independent human title/abstract screening"})
    got = {r["pmid"] for r in records}
    assert len(got) == len(records) and got == (union if complete else expected)
    assert got <= union
    priority_records = [r for r in records if r["pmid"] in expected]
    (ARC / "priority_records.json").write_text(json.dumps(priority_records, ensure_ascii=False) + "\n")
    fields = list(records[0])
    write_csv(ARC / "priority_records.csv", priority_records, fields)
    if complete:
        with gzip.open(ARC / "all_records.jsonl.gz", "wt", encoding="utf-8") as f:
            for row in records:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        with gzip.open(ARC / "all_records.csv.gz", "wt", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fields)
            writer.writeheader()
            writer.writerows(records)
    write_csv(ARC / "deduplication_map.csv", [
        {"source_query": qid, "source_pmid": p, "retained_record_id": "R-" + p,
         "rule": "Exact PMID match only; DOI/title/report-family deduplication pending"}
        for qid, ids in [("PM-CORE-20260921-R1", core), ("PM-SUPP-20260921", supp)]
        for p in sorted(ids, key=int)], ["source_query", "source_pmid", "retained_record_id", "rule"])
    write_csv(ARC / "identified_records.csv", [{"record_id": "R-" + p, "pmid": p, "in_core": p in core,
        "in_supplement": p in supp, "metadata_exported": p in got, "screening_status": "Not human-screened"}
        for p in sorted(union, key=int)], ["record_id", "pmid", "in_core", "in_supplement", "metadata_exported", "screening_status"])
    sentinel_ids = ["L-P01", "L-P02", "L-P03", "L-D01", "L-G04", "L-G05", "L-G09", "L-G10", "L-H01", "L-C03"]
    by_id = {m["id"]: m for m in existing}
    sentinels = [{"study_id": sid, "pmid": by_id[sid]["pmid"], "title": by_id[sid]["title"],
        "core": by_id[sid]["pmid"] in core, "supplement": by_id[sid]["pmid"] in supp,
        "priority_metadata": by_id[sid]["pmid"] in expected,
        "selection": "Post-execution pilot-register diagnostic, not an independent validated sentinel set"} for sid in sentinel_ids]
    write_csv(ARC / "sentinel_retrieval.csv", sentinels, list(sentinels[0]))
    categories = [
        ("Service valuation", r"relative value|\brvu|reimbursement.*procedur|procedur.*reimbursement"),
        ("Medication affordability", r"cost.related.*nonadherence|nonadherence|out.of.pocket|affordab"),
        ("Bone and fracture", r"osteoporo|bone.*dens|fracture|dxa"),
        ("Reproductive and sexual care", r"menopaus|estrogen|estradiol|vaginal|contracept|testoster|erectile"),
        ("Cardiovascular care", r"cardio|heart|coronary|stroke"),
        ("Cancer and survivorship", r"cancer|neoplasm|tumor|lymph|breast"),
        ("Mental health and pain", r"mental|psychiatr|depress|pain|opioid"),
        ("Physician-gender context", r"physician|surgeon|ophthalmolog|cardiolog"),
    ]
    ordered = sorted(priority_records, key=lambda r: hashlib.sha256(("calibration-20260921:" + r["pmid"]).encode()).hexdigest())
    selected = {}
    for row in priority_records:
        if row["existing_study_id"] in sentinel_ids:
            selected[row["pmid"]] = {**row, "sampling_reason": "Known source for calibration; not automatically included"}
    for label, regex in categories:
        matches = [r for r in ordered if re.search(regex, r["title"], re.I) and r["pmid"] not in selected]
        for row in matches[:5]:
            if len(selected) >= 50:
                break
            selected[row["pmid"]] = {**row, "sampling_reason": label + " title terms; manual classification pending"}
    for row in ordered:
        if len(selected) >= 50:
            break
        selected.setdefault(row["pmid"], {**row, "sampling_reason": "Deterministic remainder sample"})
    calibration = [{**r, "reviewer_1": "", "reviewer_1_decision": "", "reviewer_2": "", "reviewer_2_decision": "",
        "adjudication": "", "reason": "", "decision_date": ""} for r in selected.values()]
    (HERE / "calibration_50.json").write_text(json.dumps(calibration, ensure_ascii=False, indent=2) + "\n")
    write_csv(HERE / "calibration_50.csv", calibration, list(calibration[0]))
    summary = {"execution_date": "2026-09-21", "corrected_core": len(core), "supplement": len(supp),
        "duplicate_hits_removed_by_pmid": len(core & supp), "unique_identified": len(union), "metadata_exported": len(got),
        "identifier_only": len(union - got), "with_abstract": sum(bool(r["abstract"]) for r in records),
        "without_abstract": sum(not r["abstract"] for r in records),
        "calibration_records": len(calibration), "human_screened": 0,
        "sentinels_retrieved": sum(s["core"] or s["supplement"] for s in sentinels), "sentinels_total": len(sentinels),
        "not_completed": ["PRESS review", "Embase/CINAHL/EconLit/citation-index searches", *([] if complete else ["Remaining title/abstract exports"]),
            "DOI/title/report-family deduplication", "Independent human screening", "Formal risk-of-bias and certainty assessment"],
        "deduplication_rule": "Exact PMID across current core and supplementary queries; priority subset is not a third identification source",
        "calibration_sampling": "Purposive existing diagnostic sources plus up to five title-term matches per listed domain, SHA-256 deterministic order, then remainder to 50. Selection after search; not representative and not PRESS validation."}
    (HERE / "search_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
