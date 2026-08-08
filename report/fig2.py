"""Figure 2 - held-out change in precision, per method, per scanner.

Every value read directly from
  results/experiments/deterministic_postprocessing_v1/part2/reports/final_report.json
(frozen manifest 6771058f..., gold 65342ea7...).
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPORT = os.path.join(_HERE, os.pardir, "vulnerability-scanner", "results",
                       "experiments", "deterministic_postprocessing_v1", "part2",
                       "reports", "final_report.json")
R = json.load(open(_REPORT))["metrics_by_scanner"]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "DejaVu Serif"],
    "font.size": 9,
    "axes.linewidth": 0.6,
    "text.color": "#1a1a1a",
    "axes.edgecolor": "#8a8a8a",
    "axes.labelcolor": "#1a1a1a",
    "xtick.color": "#1a1a1a",
    "ytick.color": "#1a1a1a",
})

DARK, LIGHT, INK = "#3d3d3d", "#c9c9c9", "#1a1a1a"
METHODS = ["RAW", "O1_MARKDOWN", "O1_DATAFLOW", "O1_SEMANTIC",
           "O1_BASELINE_OR", "O1_CONSERVATIVE"]
SHORT = ["RAW", "MARKDOWN", "DATAFLOW", "SEMANTIC", "BASELINE-OR", "CONSERVATIVE"]

fig, (axA, axB) = plt.subplots(2, 1, figsize=(6.25, 2.85), sharex=True,
                               gridspec_kw={"hspace": 0.18})

x = list(range(len(METHODS)))
for ax, scanner, face, hatch, ylim, yt in (
        (axA, "skillspector", DARK, None, (-0.75, 5.3), [0, 2, 4]),
        (axB, "cisco", LIGHT, "////", (-0.155, 0.30), [-0.1, 0.0, 0.1, 0.2])):
    raw = 100 * R[scanner]["RAW"]["precision"]
    d = [100 * R[scanner][m]["precision"] - raw for m in METHODS]
    ax.bar(x, d, 0.46, color=face, hatch=hatch, edgecolor="white",
           linewidth=0.0, zorder=3)
    ax.axhline(0, color="#8a8a8a", lw=0.7, zorder=4)
    ax.set_ylim(*ylim)
    ax.set_yticks(yt)
    ax.yaxis.grid(True, color="#ececec", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", labelsize=7.6, length=3, width=0.6)
    ax.tick_params(axis="x", length=0)
    name = "SkillSpector" if scanner == "skillspector" else "Cisco"
    ax.text(0.006, 0.95, f"{name}   (RAW precision {raw:.2f}%)",
            transform=ax.transAxes, fontsize=8, va="top", ha="left")

# selective direct labels: the best cell, and the only cell that goes backwards
ssd = 100 * (R["skillspector"]["O1_BASELINE_OR"]["precision"]
             - R["skillspector"]["RAW"]["precision"])
cid = 100 * (R["cisco"]["O1_SEMANTIC"]["precision"] - R["cisco"]["RAW"]["precision"])
axA.annotate(f"+{ssd:.2f}", xy=(4, ssd), xytext=(0, 3), textcoords="offset points",
             ha="center", fontsize=7.8, color=INK)
axB.annotate(f"{cid:.2f}, below RAW", xy=(2.68, cid + 0.012),
             ha="right", va="top", fontsize=7.6, color=INK)

axB.set_xticks(x)
axB.set_xticklabels(SHORT, fontsize=7.6)
axB.set_xlim(-0.62, 5.62)
fig.text(0.012, 0.56, "Change in precision vs. RAW (percentage points)",
         rotation=90, va="center", ha="left", fontsize=8)

fig.subplots_adjust(left=0.105, right=0.99, top=0.985, bottom=0.115)
fig.savefig(os.path.join(_HERE, "fig2_mitigation.png"), dpi=400, facecolor="white")
print("ok")
