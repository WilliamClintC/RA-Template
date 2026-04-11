"""
theme_healy.py  --  Matplotlib / Seaborn defaults following Kieran Healy's principles

Based on:
    Healy, Kieran. 2018. *Data Visualization: A Practical Introduction.*
    Princeton University Press. https://socviz.co/

Key principles applied here (see Healy ch. 1, 3, 8):
    - Maximize data-to-ink ratio: remove top/right spines, heavy borders,
      and background fills (Healy 2018, ch. 8)
    - Use ColorBrewer "Set2" for categorical data -- perceptually uniform
      and colorblind-safe (ch. 1, 8)
    - Use viridis for continuous scales -- perceptually ordered and
      accessible across color-vision deficiencies (ch. 1)
    - Remove minor gridlines; keep major gridlines light (ch. 8)
    - Favor faceting (small multiples) over cramming groups into one
      plot with too many colors (ch. 4)
    - Always label axes clearly; include titles and source captions (ch. 1, 3)
    - Export at publication quality with explicit dimensions (ch. 8)

Import once at the top of any analysis notebook or script:
    from source.lib.theme_healy import apply_theme, PALETTE, healy_save

What this does:
    1. apply_theme() sets matplotlib rcParams for a clean, minimal look
    2. PALETTE provides a colorblind-safe categorical palette (ColorBrewer Set2)
    3. healy_save() saves figures with sensible defaults
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Categorical palette -- ColorBrewer "Set2" (colorblind-safe, up to 8)
# ---------------------------------------------------------------------------
PALETTE = [
    "#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3",
    "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3",
]

# ---------------------------------------------------------------------------
# 2. Apply theme (call once at top of script / notebook)
# ---------------------------------------------------------------------------
def apply_theme(font_size=12):
    """Set matplotlib rcParams following Healy's principles."""
    mpl.rcParams.update({
        # Figure
        "figure.figsize":       (6, 4),
        "figure.dpi":           150,
        "figure.facecolor":     "white",
        "savefig.dpi":          300,
        "savefig.bbox":         "tight",
        "savefig.facecolor":    "white",

        # Font
        "font.size":            font_size,
        "font.family":          "sans-serif",
        "axes.titlesize":       font_size * 1.15,
        "axes.titleweight":     "bold",
        "axes.labelsize":       font_size * 0.9,

        # Axes
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "axes.edgecolor":       "grey70",
        "axes.linewidth":       0.6,
        "axes.grid":            True,
        "axes.grid.which":      "major",
        "axes.prop_cycle":      mpl.cycler(color=PALETTE),

        # Grid
        "grid.color":           "#e5e5e5",
        "grid.linewidth":       0.4,

        # Ticks
        "xtick.color":          "grey30",
        "ytick.color":          "grey30",
        "xtick.labelsize":      font_size * 0.8,
        "ytick.labelsize":      font_size * 0.8,

        # Legend
        "legend.frameon":       False,
        "legend.fontsize":      font_size * 0.8,
    })

    # If seaborn is available, set its defaults too
    try:
        import seaborn as sns
        sns.set_palette(PALETTE)
    except ImportError:
        pass


# ---------------------------------------------------------------------------
# 3. Save helper
# ---------------------------------------------------------------------------
def healy_save(fig, filepath, width=6, height=4, dpi=300, **kwargs):
    """Save a figure with publication-quality defaults."""
    fig.set_size_inches(width, height)
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight",
                facecolor="white", **kwargs)
