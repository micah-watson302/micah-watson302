import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

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


def ease(t: float) -> float:
    # smoothstep
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def save_gif(frames, path: Path, duration=70):
    imgs = [Image.open(p).convert("P", palette=Image.ADAPTIVE) for p in frames]
    imgs[0].save(
        path,
        save_all=True,
        append_images=imgs[1:],
        duration=duration,
        loop=0,
        optimize=True,
    )
    for p in frames:
        p.unlink(missing_ok=True)


# ---------- static PNG + animated GIF: commits by year ----------
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

tmpdir = out / "_frames"
tmpdir.mkdir(exist_ok=True)
frame_paths = []
n_frames = 24
for i in range(n_frames):
    t = ease(i / (n_frames - 1))
    fig, ax = plt.subplots(figsize=(11, 3.6), dpi=110)
    style(ax)
    vals = [c * t for c in counts]
    ax.bar(years, vals, color=lime, width=0.72)
    if t > 0.85:
        for x, c in zip(years, counts):
            ax.text(x, c + 6, str(c), ha="center", va="bottom", color=white, fontsize=8)
    ax.set_title("commits by year", loc="left", fontsize=13, pad=10)
    ax.set_xticks(years)
    ax.set_ylim(0, max(counts) * 1.18)
    fig.tight_layout()
    fp = tmpdir / f"year_{i:02d}.png"
    fig.savefig(fp, facecolor=bg, edgecolor="none")
    plt.close()
    frame_paths.append(fp)
# hold last frame a bit longer by duplicating
frame_paths.extend([frame_paths[-1]] * 8)
save_gif(frame_paths, out / "commits-by-year.gif", duration=60)

# ---------- recent months ----------
labels = list("JFMAMJJASOND") + list("JFMAMJJASON")
vals_m = [14, 13, 24, 43, 31, 28, 25, 28, 29, 33, 25, 20, 13, 5, 16, 28, 28, 35, 17, 29, 30, 26, 3]
colors = [lime] * 12 + [teal] * 11

fig, ax = plt.subplots(figsize=(11, 3.4), dpi=140)
style(ax)
ax.bar(range(len(vals_m)), vals_m, color=colors, width=0.8)
ax.set_xticks(range(len(vals_m)))
ax.set_xticklabels(labels, color=muted)
ax.set_title("recent monthly velocity  (lime=2025  teal=2026)", loc="left", fontsize=12, pad=10)
ax.set_ylim(0, max(vals_m) * 1.2)
fig.tight_layout()
fig.savefig(out / "commits-recent.png", facecolor=bg, edgecolor="none")
plt.close()

frame_paths = []
n_frames = 26
for i in range(n_frames):
    # reveal bars left-to-right
    reveal = ease(i / (n_frames - 1)) * len(vals_m)
    shown = []
    cols = []
    for idx, v in enumerate(vals_m):
        if idx + 1 <= reveal:
            shown.append(v)
            cols.append(colors[idx])
        elif idx < reveal:
            frac = reveal - idx
            shown.append(v * frac)
            cols.append(colors[idx])
        else:
            shown.append(0)
            cols.append(colors[idx])
    fig, ax = plt.subplots(figsize=(11, 3.4), dpi=110)
    style(ax)
    ax.bar(range(len(shown)), shown, color=cols, width=0.8)
    ax.set_xticks(range(len(vals_m)))
    ax.set_xticklabels(labels, color=muted)
    ax.set_title("recent monthly velocity  (lime=2025  teal=2026)", loc="left", fontsize=12, pad=10)
    ax.set_ylim(0, max(vals_m) * 1.2)
    fig.tight_layout()
    fp = tmpdir / f"month_{i:02d}.png"
    fig.savefig(fp, facecolor=bg, edgecolor="none")
    plt.close()
    frame_paths.append(fp)
frame_paths.extend([frame_paths[-1]] * 8)
save_gif(frame_paths, out / "commits-recent.gif", duration=55)

# ---------- weekdays ----------
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

frame_paths = []
n_frames = 22
for i in range(n_frames):
    t = ease(i / (n_frames - 1))
    cur = [v * t for v in dvals]
    fig, ax = plt.subplots(figsize=(11, 3.2), dpi=110)
    style(ax)
    ax.barh(days[::-1], cur[::-1], color=dcols[::-1], height=0.65)
    if t > 0.85:
        for y, v in enumerate(dvals[::-1]):
            ax.text(v + 4, y, str(v), va="center", color=white, fontsize=9)
    ax.set_title("commits by weekday", loc="left", fontsize=13, pad=10)
    ax.set_xlim(0, max(dvals) * 1.15)
    fig.tight_layout()
    fp = tmpdir / f"week_{i:02d}.png"
    fig.savefig(fp, facecolor=bg, edgecolor="none")
    plt.close()
    frame_paths.append(fp)
frame_paths.extend([frame_paths[-1]] * 8)
save_gif(frame_paths, out / "commits-by-weekday.gif", duration=60)

try:
    tmpdir.rmdir()
except OSError:
    pass

for p in [
    "commits-by-year.png",
    "commits-by-year.gif",
    "commits-recent.png",
    "commits-recent.gif",
    "commits-by-weekday.png",
    "commits-by-weekday.gif",
]:
    print(p, (out / p).stat().st_size)
print("done")
