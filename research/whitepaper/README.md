# White-paper PDF

`build_whitepaper.py` creates the September 16, 2026 preliminary white paper, its Markdown manuscript, four figures (PNG and SVG), and a manifest in the project's existing output directory.

Install `reportlab`, `matplotlib`, and `pypdf` in a Python environment, then run from the repository root:

```sh
python research/whitepaper/build_whitepaper.py
```

The builder uses the curated reference registry, synthesis data, and procedure-pair extraction. It checks the plan-segment denominators, recomputes RVU differences, and verifies that all cited scientific and methodology records retain PMIDs. It does not perform a new systematic search or a formal certainty assessment.

Version 1.1 expands Methods to three pages (PDF pages 3-5): design and eligibility; source identification, extraction and synthesis; and exact CMS join keys, denominators, drug matching, formulary states and RVU calculations. Completed analyses are distinguished from the remaining systematic-review procedures. The evidence counts and four figures are unchanged.

Render the PDF with Poppler and inspect every page before releasing a regenerated version. A new build resets the manifest's visual-review status. The figure SVGs preserve editable vector elements; the PDF embeds high-resolution figure images.

Figure 3 follows the published comparator order. The historical `male` and `female` JSON keys are retained for traceability, but the figure uses first-code/second-code labels: CPT 51597 is not exclusive to male patients. See P-045 for the classification source.

The full living bibliography and RIS export include additional active, contextual and excluded records. The paper's bibliography contains the sources cited in the paper.
