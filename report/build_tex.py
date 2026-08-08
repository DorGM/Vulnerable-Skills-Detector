"""Convert the report docx into a two-column IEEEtran paper.

Text is taken verbatim from the docx — nothing is retyped — so the LaTeX
cannot drift from the source. Structural additions are explicit and listed
in ADDED below.

ADDED (not present in the docx):
  * title and IEEE author block
  * Fig. 1 / Fig. 2 and their captions and in-text references
  * a blue repo link under the title
  * bracketed \\cite{} citations in place of literal "[n]" in the body
"""
import os
import re
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

import sys
# Path to the source Word report (not committed -- pass it as argv[1]).
SRC = sys.argv[1] if len(sys.argv) > 1 else "cyber skills vuln report.docx"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "Vulnerable-Skills-Detector-Report.tex")
REPO = "https://github.com/AvinoamNukrai/Vulnerable-Skills-Detector"
TITLE = ("Auditing the Auditors: Agreement, Precision, and Blind Spots of "
         "Vendor Scanners for AI Agent Skills")

# ------------------------------------------------------------------ escaping
_math = []


def _stash(latex):
    _math.append(latex)
    return f"@@M{len(_math) - 1}@@"


def to_latex(text):
    t = text.replace("\u200b", "")
    t = re.sub(r"pHolm", lambda m: _stash(r"$p_{\mathrm{Holm}}$"), t)
    t = re.sub(r"\u00d710\u2212(\d+)",
               lambda m: _stash(rf"$\times 10^{{-{m.group(1)}}}$"), t)
    t = t.replace("\u2248", _stash(r"$\approx$"))
    t = t.replace("\u2212", _stash("$-$"))
    t = t.replace("\u2013", _stash("--"))

    for ch, rep in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                    ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                    ("}", r"\}"), ("~", r"\textasciitilde{}"),
                    ("^", r"\textasciicircum{}")):
        t = t.replace(ch, rep)

    # straight quotes -> TeX quotes
    t = re.sub(r'"([^"]*)"', r"``\1''", t)
    for i, m in enumerate(_math):
        t = t.replace(f"@@M{i}@@", m)
    return t


def body_latex(text):
    """Body paragraph: escape, then turn literal [n] into \\cite{refn}."""
    t = to_latex(text)
    t = re.sub(r"\[(\d+)\]", r"\\cite{ref\1}", t)
    return t


# ------------------------------------------------------------------ read docx
doc = Document(SRC)
blocks = []
for child in doc.element.body.iterchildren():
    if child.tag.endswith("}p"):
        p = Paragraph(child, doc)
        if p.text.strip():
            blocks.append(("p", p.style.name, p.text.strip()))
    elif child.tag.endswith("}tbl"):
        tb = Table(child, doc)
        blocks.append(("t", None,
                       [[c.text.strip().replace("\n", " ") for c in r.cells]
                        for r in tb.rows]))

# ------------------------------------------------------------------- figures
FIG1 = r"""
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{fig1_agreement.png}
\caption{Scanner agreement at three levels of abstraction. Each bar is
normalized to the units either scanner produced at that level: 1,538 distinct
category-rule-file keys, the 342 skills flagged by at least one scanner (the
remaining 393 of 735 are clean for both), and the 29 neutral threat classes
reached through the taxonomy bridge. Agreement is zero on exact rule identity,
30\% at the skill level and 45\% at the class level; within the 102 jointly
flagged skills the bridge recovers 127 shared skill-class pairs.}
\label{fig:agreement}
\end{figure*}
"""

FIG2 = r"""
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{fig2_mitigation.png}
\caption{Change in precision from deterministic post-processing on the
400-finding held-out test set (396 adjudicated), relative to each scanner's RAW
baseline. The scanners are plotted separately because their RAW baselines
differ by a factor of 2.6 and the Cisco effects are an order of magnitude
smaller, so a shared axis would hide them. Only O1-SEMANTIC and the
O1-BASELINE-OR policy that subsumes it move SkillSpector precision appreciably,
by $+4.11$ points; on Cisco every effect is under a quarter of a point, and
O1-SEMANTIC alone moves precision backwards, from 5.05\% to 4.97\%.}
\label{fig:mitigation}
\end{figure*}
"""


def table1(rows):
    head, data = rows[0], rows[1:]
    out = [r"\begin{table*}[t]", r"\caption{This work against the closest prior "
           r"art. GT = labelled ground truth.}", r"\label{tab:related}",
           r"\centering\footnotesize",
           r"\setlength{\tabcolsep}{5pt}\renewcommand{\arraystretch}{1.15}",
           r"\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.6cm}"
           r">{\raggedright\arraybackslash}p{2.5cm}"
           r">{\raggedright\arraybackslash}p{3.4cm}"
           r">{\raggedright\arraybackslash}p{2.6cm}"
           r">{\raggedright\arraybackslash}p{1.9cm}"
           r">{\raggedright\arraybackslash}p{1.5cm}@{}}", r"\toprule",
           " & ".join(rf"\textbf{{{to_latex(h)}}}" for h in head) + r" \\",
           r"\midrule"]
    for r in data:
        cells = [body_latex(c) for c in r]
        if r[0].startswith("This work"):
            cells[0] = r"\textbf{This work}"
        out.append(" & ".join(cells) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    return "\n".join(out)


def table2(rows):
    head, data = rows[0], rows[1:]
    out = [r"\begin{table}[t]",
           r"\caption{Held-out performance of every post-processing method on "
           r"each scanner (400-finding blind test set, 396 adjudicated).}",
           r"\label{tab:heldout}", r"\centering\footnotesize",
           r"\setlength{\tabcolsep}{3.5pt}",
           r"\begin{tabular}{@{}llrrrr@{}}", r"\toprule",
           r"\textbf{Scanner} & \textbf{Method} & \textbf{Prec.} & "
           r"\textbf{FP supp.} & \textbf{TP ret.} & \textbf{Abst.} \\",
           r"\midrule"]
    for i, r in enumerate(data):
        if i == 6:
            out.append(r"\midrule")
        out.append(" & ".join(to_latex(c) for c in r) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(out)


# --------------------------------------------------------------- assemble
L = []
abstract, refs = [], []
mode = "front"
pending_table_caption = False
ti = 0

for kind, style, payload in blocks:
    if kind == "t":
        ti += 1
        L.append(table1(payload) if ti == 1 else table2(payload))
        continue

    text = payload
    if style == "Heading 1":
        name = re.sub(r"^\d+\.\s*", "", text).strip()
        if name.lower() == "abstract":
            mode = "abstract"
            continue
        if name.lower() == "references":
            mode = "refs"
            continue
        mode = "body"
        L.append(r"\section{%s}" % to_latex(name))
        continue

    if style == "Heading 2":
        name = re.sub(r"^\d+\.\d+\s*", "", text).strip()
        L.append(r"\subsection{%s}" % to_latex(name))
        continue

    if mode == "front":
        continue  # docx title / author lines -> replaced by the IEEE title block
    if mode == "abstract":
        abstract.append(text)
        continue
    if mode == "refs":
        refs.append(text)
        continue

    # ---- body paragraph
    if re.fullmatch(r"[0-9a-f]{64}", text):
        L.append(r"\begin{center}\ttfamily\footnotesize %s\\ %s\end{center}"
                 % (text[:32], text[32:]))
        continue
    if text.startswith("Table 1."):
        continue  # became the table caption

    para = body_latex(text)

    if text.startswith("At the level of exact category-rule-file keys"):
        para += (" Fig.~\\ref{fig:agreement} shows the three levels of "
                 "comparison side by side.")
    if text.startswith("The taxonomy bridge changes the interpretation"):
        L.append(FIG1)
    if text.startswith("The semantic-context component accounts for most"):
        para += (" Fig.~\\ref{fig:mitigation} shows the resulting change in "
                 "precision for every method and scanner.")
        L.append(FIG2)
    if text.startswith("Table 1 places this work"):
        para = para.replace("Table 1 places", "Table~\\ref{tab:related} places")

    L.append(para)

# --------------------------------------------------------------- references
bib = [r"\begin{thebibliography}{99}"]
for r in refs:
    m = re.match(r"\[(\d+)\]\s*(.*)", r, re.S)
    n, rest = m.group(1), m.group(2).strip()
    url = None
    um = re.search(r"Available:\s*(\S+)", rest)
    if um:
        url = um.group(1).rstrip(".")
        rest = rest[:um.start()].rstrip()
    rest = re.sub(r"\[Online\]\.?\s*$", "", rest).rstrip()
    body = to_latex(rest)
    if url:
        body += r" [Online]. Available: \url{%s}" % url
    bib.append(r"\bibitem{ref%s} %s" % (n, body))
bib.append(r"\end{thebibliography}")

# --------------------------------------------------------------- preamble
ABSTRACT = " ".join(to_latex(a) for a in abstract)

doc_tex = r"""%% Generated from "cyber skills vuln report.docx" -- body text verbatim.
\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts
\usepackage{cite}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{amsmath,amssymb}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{url}
\usepackage{xurl}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage[hidelinks,breaklinks]{hyperref}
\urlstyle{same}
\sloppy

%% arabic section numbers, left-aligned and bold (not IEEE's centered roman)
\renewcommand{\thesection}{\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\titleformat{\section}[block]
  {\normalfont\large\bfseries\raggedright}{\thesection.}{0.5em}{}
\titleformat{\subsection}[block]
  {\normalfont\normalsize\bfseries\raggedright}{\thesubsection}{0.5em}{}
\titlespacing*{\section}{0pt}{2.2ex plus 1ex minus .2ex}{1.0ex plus .2ex}
\titlespacing*{\subsection}{0pt}{1.8ex plus .8ex minus .2ex}{0.7ex plus .2ex}
\renewcommand{\IEEEbibitemsep}{0pt}

\begin{document}

\title{%(title)s\\[0.45em]
\normalfont\normalsize\href{%(repo)s}{\textcolor{blue}{%(repo)s}}}

\author{%%
\IEEEauthorblockN{Avinoam Nukrai - 206997132 \quad Ori Sinvani - 325770824
\quad Dor Meir - 313254724}
\IEEEauthorblockA{Methods for Detecting Cyber Attacks (372-2-5203)}%%
}

\maketitle

\begin{abstract}
\normalfont\mdseries\normalsize
%(abstract)s
\end{abstract}

%(bodytext)s

%(bib)s

\end{document}
""" % {
    "title": TITLE,
    "repo": REPO,
    "abstract": ABSTRACT,
    "bodytext": "\n\n".join(L),
    "bib": "\n".join(bib),
}

open(OUT, "w").write(doc_tex)
print("wrote", OUT, len(doc_tex), "chars;", len(refs), "refs;", ti, "tables")
