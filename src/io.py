"""I/O utilities for loading and saving datasets."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from src import config


def load_raw_transactions(path: Path | None = None) -> pd.DataFrame:
    """Load raw Online Retail II data with a friendly error if missing."""
    raw_path = path or config.RAW_DATA_PATH
    if raw_path.exists():
        return pd.read_csv(raw_path)

    if path is None and config.RAW_XLSX_PATH.exists():
        df = pd.read_excel(config.RAW_XLSX_PATH)
        # Standardize column names from Excel file
        df = df.rename(columns={
            "Price": "UnitPrice",
            "Customer ID": "CustomerID"
        })
        return df

    missing_hint = (
        f"Raw data not found at {raw_path}. "
        "Place 'online_retail_ii.csv' or 'online_retail_II.xlsx' into data/raw/ before running."
    )
    raise FileNotFoundError(missing_hint)


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    """Save a DataFrame to CSV, ensuring parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
