"""Figure 1 - scanner agreement at three granularities.

All values verified against:
  results/cross_scanner_report.md      (keys 1207/331/0; skills 102/225/15/393)
  results/taxonomy_coverage.json       (classes 13 both / 11 SS-only / 5 Cisco-only;
                                        skill_class_pairs_flagged_by_both = 127)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "DejaVu Serif"],
    "font.size": 9,
    "axes.linewidth": 0.6,
    "text.color": "#1a1a1a",
    "axes.edgecolor": "#8a8a8a",
    "axes.labelcolor": "#1a1a1a",
    "xtick.color": "#8a8a8a",
    "ytick.color": "#1a1a1a",
})

SS_ONLY, BOTH, CI_ONLY = "#d9d9d9", "#3d3d3d", "#a6a6a6"
SURFACE = "white"

rows = [
    # label, n-note, ss_only, both, cisco_only
    ("Exact rule identity\ncategory-rule-file keys",
     "n = 1,538", 1207, 0, 331),
    ("Skill level\nskills flagged by either scanner",
     "n = 342", 225, 102, 15),
    ("Neutral threat class\nclasses reached via the taxonomy bridge",
     "n = 29", 11, 13, 5),
]

fig, ax = plt.subplots(figsize=(6.25, 2.55))
h = 0.46
ypos = [2, 1, 0]

for y, (_, _, a, b, c) in zip(ypos, rows):
    tot = a + b + c
    fa, fb, fc = 100 * a / tot, 100 * b / tot, 100 * c / tot
    # 2px surface gap between adjacent fills, no borders around marks
    ax.barh(y, fa, height=h, color=SS_ONLY, zorder=3)
    ax.barh(y, fb, left=fa, height=h, color=BOTH, zorder=3)
    ax.barh(y, fc, left=fa + fb, height=h, color=CI_ONLY,
            hatch="////", edgecolor=SURFACE, linewidth=0, zorder=3)
    for x0 in (fa, fa + fb):
        ax.barh(y, 0.55, left=x0 - 0.28, height=h, color=SURFACE, zorder=4)

    # selective direct labels; segments too narrow to hold a label get it above
    for val, frac, x0, ink in ((a, fa, 0, "#1a1a1a"),
                               (b, fb, fa, "white"),
                               (c, fc, fa + fb, "#1a1a1a")):
        if not val:
            continue
        if frac >= 7:
            ax.text(x0 + frac / 2, y, f"{val:,}", ha="center", va="center",
                    color=ink, fontsize=8.5, zorder=6)
        else:
            ax.text(x0 + frac / 2, y + h / 2 + 0.06, f"{val:,}", ha="center",
                    va="bottom", color="#1a1a1a", fontsize=7.6, zorder=6)
    # the funnel: share agreed on, at the right margin
    ax.text(102, y, f"{fb:.0f}%" if b else "0%", ha="left", va="center",
            fontsize=9.5, color="#1a1a1a", fontweight="bold", zorder=6)

ax.set_yticks(ypos)
ax.set_yticklabels([f"{lab}\n({n})" for lab, n, *_ in rows],
                   fontsize=8.2, linespacing=1.35)
ax.set_xlim(0, 100)
ax.set_ylim(-0.52, 2.72)
ax.set_xlabel("Share of compared units (%)", fontsize=8.5, labelpad=4)
ax.set_xticks([0, 25, 50, 75, 100])
ax.xaxis.set_tick_params(labelsize=8, length=3, width=0.6)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.grid(True, color="#e6e6e6", linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)

ax.text(102, 2.50, "shared", ha="left", va="bottom",
        fontsize=7.8, color="#6b6b6b", style="italic")

ax.legend(handles=[
    Patch(facecolor=SS_ONLY, label="SkillSpector only"),
    Patch(facecolor=BOTH, label="Both scanners"),
    Patch(facecolor=CI_ONLY, hatch="////", edgecolor="white", label="Cisco only"),
], loc="lower center", bbox_to_anchor=(0.44, -0.40), ncol=3, frameon=False,
    fontsize=8.2, handlelength=1.5, handleheight=0.9, columnspacing=1.6)

fig.subplots_adjust(left=0.335, right=0.925, top=0.97, bottom=0.28)
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig1_agreement.png"), dpi=400, facecolor="white")
print("ok")
