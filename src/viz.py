"""Visualization helpers."""
from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def set_plot_style() -> None:
    """Apply a consistent plotting style."""
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({"figure.dpi": 120, "savefig.dpi": 120})


def save_fig(path: Path) -> None:
    """Save the current matplotlib figure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")


def barplot_segments(segment_counts: pd.DataFrame, title: str) -> None:
    """Create a bar plot for segment counts."""
    sns.barplot(data=segment_counts, x="RFM_SEGMENT", y="customers", palette="viridis")
    plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.xlabel("Segment")
    plt.ylabel("Customers")


def heatmap_table(table: pd.DataFrame, title: str, fmt: str = ".0%") -> None:
    """Create a heatmap from a cohort table."""
    sns.heatmap(table, annot=True, fmt=fmt, cmap="Blues")
    plt.title(title)
    plt.xlabel("Cohort Index")
    plt.ylabel("Cohort Month")
