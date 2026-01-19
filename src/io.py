"""I/O utilities for loading and saving datasets."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from src import config


def load_raw_transactions(path: Path | None = None) -> pd.DataFrame:
    """Load raw Online Retail II data with a friendly error if missing."""
    raw_path = path or config.RAW_DATA_PATH
    if not raw_path.exists():
        raise FileNotFoundError(
            f"Raw data not found at {raw_path}. "
            "Please place 'online_retail_ii.csv' into data/raw/ before running."
        )
    return pd.read_csv(raw_path)


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    """Save a DataFrame to CSV, ensuring parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
