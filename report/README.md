# Report

Final write-up for the project: *Auditing the Auditors — Agreement, Precision,
and Blind Spots of Vendor Scanners for AI Agent Skills*.

| File | What it is |
|------|------------|
| `Vulnerable-Skills-Detector-Report.pdf` | The compiled report, 11 pages, IEEE two-column |
| `Vulnerable-Skills-Detector-Report.tex` | LaTeX source (`IEEEtran`, `conference` option) |
| `fig1_agreement.png` | Fig. 1 — scanner agreement at three levels of abstraction |
| `fig2_mitigation.png` | Fig. 2 — change in precision from deterministic post-processing |
| `fig1.py`, `fig2.py` | Scripts that generate the two figures |
| `build_tex.py` | Script that generates the `.tex` from the Word source |

## Building the PDF

```
pdflatex Vulnerable-Skills-Detector-Report.tex     # run three times, to settle cross-references and floats
```

Needs `IEEEtran.cls` (Debian/Ubuntu: `texlive-publishers`) plus `cite`,
`graphicx`, `booktabs`, `array`, `amsmath`, `url`, `xurl`, `xcolor`,
`titlesec` and `hyperref`.

## Regenerating the figures

```
python3 fig1.py
python3 fig2.py
```

`fig2.py` reads its numbers at runtime from

```
../vulnerability-scanner/results/experiments/deterministic_postprocessing_v1/part2/reports/final_report.json
```

so the figure cannot drift from the committed held-out results. `fig1.py`
carries its counts inline, each annotated with the results file it came from
(`results/cross_scanner_report.md` and `results/taxonomy_coverage.json`).

## Regenerating the LaTeX

`Vulnerable-Skills-Detector-Report.tex` is generated, not hand-written. `build_tex.py` reads the Word
report and emits the LaTeX — body text, both tables and all 22 references are
extracted programmatically, so the two cannot diverge.

```
python3 build_tex.py "path/to/cyber skills vuln report.docx"
```

The source `.docx` is not committed here. If you edit the `.tex` by hand,
either fold the same change back into the `.docx` or accept that the next
regeneration will overwrite it.

What `build_tex.py` adds on top of the Word document: the title, the repo link
below it, the author block, the two figures with captions and in-text
references, and `\cite{}` markup in place of the literal `[n]` citations in the
body.
