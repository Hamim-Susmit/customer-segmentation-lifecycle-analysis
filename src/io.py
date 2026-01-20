"""I/O utilities for loading and saving datasets."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from src import config


def load_raw_transactions(path: Path | None = None) -> pd.DataFrame:
    """Load raw Online Retail II data with a friendly error if missing."""
    if path is not None:
        return _load_by_extension(path)

    if config.RAW_DATA_CSV.exists():
        return pd.read_csv(config.RAW_DATA_CSV)
    if config.RAW_DATA_XLSX.exists():
        return pd.read_excel(config.RAW_DATA_XLSX)

    raise FileNotFoundError(
        "Raw data not found. Please place 'online_retail_ii.csv' or "
        "'online_retail_ii.xlsx' into data/raw/ before running."
    )


def _load_by_extension(path: Path) -> pd.DataFrame:
    """Load a dataset based on file extension."""
    if not path.exists():
        raise FileNotFoundError(f"Raw data not found at {path}.")
    if path.suffix.lower() == ".xlsx":
        return pd.read_excel(path)
    return pd.read_csv(path)


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    """Save a DataFrame to CSV, ensuring parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
