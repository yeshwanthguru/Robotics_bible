"""Shared helpers for generating the book's figures.

Run `python tools/figures/make_all.py` (needs matplotlib + numpy) to regenerate
every SVG into static/img/fig/.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon, Ellipse
import numpy as np

BLUE, ORANGE, GREEN, RED, PURPLE, GRAY, TEAL, YELLOW = (
    "#2e6bd6", "#f08a24", "#2ca25f", "#d64545", "#7b5cd6", "#6b7280", "#14a3a3", "#e6b422")
LIGHT = {BLUE: "#e3edfc", ORANGE: "#fdeedd", GREEN: "#def3e7", RED: "#fbe4e4",
         PURPLE: "#ece7fb", GRAY: "#eceef1", TEAL: "#dcf3f3", YELLOW: "#fbf3d6"}
INK = "#1f2937"

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "static", "img", "fig")
PREVIEW = os.environ.get("FIG_PREVIEW")  # optional dir for PNG previews

plt.rcParams.update({
    "svg.fonttype": "path", "font.family": "DejaVu Sans", "font.size": 11,
    "axes.edgecolor": "#9ca3af", "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": "#4b5563", "ytick.color": "#4b5563", "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.titleweight": "bold", "axes.titlesize": 12,
})


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, name + ".svg"), bbox_inches="tight", facecolor="white")
    if PREVIEW:
        os.makedirs(PREVIEW, exist_ok=True)
        fig.savefig(os.path.join(PREVIEW, name + ".png"), bbox_inches="tight", dpi=70, facecolor="white")
    plt.close(fig)


def canvas(w=10, h=5, xlim=(0, 100), ylim=(0, 50)):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off"); ax.set_aspect("auto")
    return fig, ax


def box(ax, x, y, w, h, text, color=BLUE, fs=10.5, bold=False, dashed=False, tc=None):
    """Rounded box centred at (x, y)."""
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                       fc=LIGHT[color], ec=color, lw=1.6, ls="--" if dashed else "-")
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc or INK,
            fontweight="bold" if bold else "normal", linespacing=1.25)


def arrow(ax, p1, p2, text=None, color=GRAY, rad=0.0, lw=1.8, fs=9.5, dy=1.6, dx=0, style="-|>", ls="-"):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14, lw=lw, color=color,
                        connectionstyle=f"arc3,rad={rad}", ls=ls, shrinkA=2, shrinkB=2)
    ax.add_patch(a)
    if text:
        ax.text((p1[0] + p2[0]) / 2 + dx, (p1[1] + p2[1]) / 2 + dy, text, ha="center", va="bottom",
                fontsize=fs, color=color if color != GRAY else "#4b5563")


def label(ax, x, y, text, fs=10, color=INK, ha="center", va="center", bold=False, **kw):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color,
            fontweight="bold" if bold else "normal", **kw)


def title(ax, text, y=48, fs=13):
    ax.text(50, y, text, ha="center", va="center", fontsize=fs, fontweight="bold", color=INK)
