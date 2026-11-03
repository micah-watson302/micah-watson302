import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

out = Path(__file__).resolve().parent
bg = "#0a0a0a"
lime = "#b6ff3b"
teal = "#7dd3c7"
muted = "#777777"
white = "#eaeaea"


def style(ax):
    ax.set_facecolor(bg)
    ax.figure.patch.set_facecolor(bg)
    ax.tick_params(colors=muted)
    for s in ax.spines.values():
        s.set_color("#222222")
    ax.title.set_color(lime)


years = list(range(2016, 2027))
counts = [21, 33, 38, 73, 68, 115, 191, 220, 253, 313, 230]
fig, ax = plt.subplots(figsize=(11, 3.6), dpi=140)
style(ax)
bars = ax.bar(years, counts, color=lime, width=0.72)
for b, c in zip(bars, counts):
    ax.text(b.get_x() + b.get_width() / 2, c + 6, str(c), ha="center", va="bottom", color=white, fontsize=8)
ax.set_title("commits by year", loc="left", fontsize=13, pad=10)
ax.set_xticks(years)
ax.set_ylim(0, max(counts) * 1.18)
ax.annotate("total tracked ~ 1555", xy=(0.99, 0.02), xycoords="axes fraction", ha="right", color=muted, fontsize=8)
fig.tight_layout()
fig.savefig(out / "commits-by-year.png", facecolor=bg, edgecolor="none")
plt.close()

labels = list("JFMAMJJASOND") + list("JFMAMJJASON")
vals = [14, 13, 24, 43, 31, 28, 25, 28, 29, 33, 25, 20, 13, 5, 16, 28, 28, 35, 17, 29, 30, 26, 3]
colors = [lime] * 12 + [teal] * 11
fig, ax = plt.subplots(figsize=(11, 3.4), dpi=140)
style(ax)
ax.bar(range(len(vals)), vals, color=colors, width=0.8)
ax.set_xticks(range(len(vals)))
ax.set_xticklabels(labels, color=muted)
ax.set_title("recent monthly velocity  (lime=2025  teal=2026)", loc="left", fontsize=12, pad=10)
ax.set_ylim(0, max(vals) * 1.2)
fig.tight_layout()
fig.savefig(out / "commits-recent.png", facecolor=bg, edgecolor="none")
plt.close()

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
dvals = [328, 312, 284, 303, 238, 48, 42]
dcols = [lime, lime, lime, lime, lime, "#555555", "#444444"]
fig, ax = plt.subplots(figsize=(11, 3.2), dpi=140)
style(ax)
ax.barh(days[::-1], dvals[::-1], color=dcols[::-1], height=0.65)
for y, v in enumerate(dvals[::-1]):
    ax.text(v + 4, y, str(v), va="center", color=white, fontsize=9)
ax.set_title("commits by weekday", loc="left", fontsize=13, pad=10)
ax.set_xlim(0, max(dvals) * 1.15)
fig.tight_layout()
fig.savefig(out / "commits-by-weekday.png", facecolor=bg, edgecolor="none")
plt.close()

for p in ["commits-by-year.png", "commits-recent.png", "commits-by-weekday.png"]:
    print(p, (out / p).stat().st_size)
print("done")
