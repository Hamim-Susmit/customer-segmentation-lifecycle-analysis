"""I/O utilities for loading and saving datasets."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from src import config


def load_raw_transactions(path: Path | None = None) -> pd.DataFrame:
    """Load raw Online Retail II data with a friendly error if missing."""
    if path is not None:
        return _load_by_extension(path)

    candidates = [
        config.RAW_DATA_CSV,
        config.RAW_DATA_XLSX,
        config.RAW_DATA_CSV_ALT,
        config.RAW_DATA_XLSX_ALT,
    ]
    for candidate in candidates:
        if candidate.exists():
            return _load_by_extension(candidate)

    raise FileNotFoundError(
        "Raw data not found. Please place 'online_retail_ii.csv', "
        "'online_retail_ii.xlsx', 'online_retail_II.csv', or "
        "'online_retail_II.xlsx' into data/raw/ before running."
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
