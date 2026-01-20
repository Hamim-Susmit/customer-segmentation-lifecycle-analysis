"""RFM scoring and segmentation."""
from __future__ import annotations

import pandas as pd


SEGMENT_MAP = {
    r"555": "Champions",
    r"[4-5][4-5][4-5]": "Loyal",
    r"[4-5][3-4][3-4]": "Potential Loyalist",
    r"5[1-2][1-2]": "New",
    r"4[1-2][1-2]": "Promising",
    r"3[2-3][2-3]": "Needs Attention",
    r"[1-2][2-3][2-3]": "At Risk",
    r"[1-2][1-2][1-2]": "Hibernating",
}


def score_rfm(customer_df: pd.DataFrame, n_tiles: int = 5) -> pd.DataFrame:
    """Score customers using quantile-based RFM scoring."""
    df = customer_df.copy()
    df["R"] = pd.qcut(df["recency_days"], n_tiles, labels=False, duplicates="drop")
    df["R"] = df["R"].max() - df["R"] + 1
    df["F"] = pd.qcut(df["frequency"].rank(method="first"), n_tiles, labels=False) + 1
    df["M"] = pd.qcut(df["monetary"].rank(method="first"), n_tiles, labels=False) + 1
    df["RFM_SCORE"] = df[["R", "F", "M"]].astype(int).astype(str).agg("".join, axis=1)
    return df


def assign_rfm_segments(customer_scored: pd.DataFrame) -> pd.DataFrame:
    """Assign descriptive RFM segments based on RFM_SCORE pattern."""
    df = customer_scored.copy()
    df["RFM_SEGMENT"] = "Other"
    for pattern, label in SEGMENT_MAP.items():
        df.loc[df["RFM_SCORE"].str.match(pattern), "RFM_SEGMENT"] = label
    return df
