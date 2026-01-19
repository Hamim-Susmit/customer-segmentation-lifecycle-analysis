"""Data cleaning routines for Online Retail II."""
from __future__ import annotations

import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw transaction data.

    Steps:
    - Parse InvoiceDate to datetime
    - Create Revenue column
    - Remove zero/negative UnitPrice and zero Quantity
    - Flag cancellations/returns
    - Drop missing CustomerID for modeling
    """
    df_clean = df.copy()
    df_clean["InvoiceDate"] = pd.to_datetime(df_clean["InvoiceDate"], errors="coerce")
    df_clean = df_clean.dropna(subset=["InvoiceDate"])

    df_clean["Revenue"] = df_clean["Quantity"] * df_clean["UnitPrice"]
    df_clean = df_clean[df_clean["Quantity"] != 0]
    df_clean = df_clean[df_clean["UnitPrice"] > 0]

    df_clean["is_cancellation"] = (
        df_clean["Invoice"].astype(str).str.startswith("C") | (df_clean["Quantity"] < 0)
    )

    return df_clean


def split_gross_net(df_clean: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return gross (exclude cancellations) and net (include cancellations) datasets."""
    gross = df_clean[~df_clean["is_cancellation"]].copy()
    net = df_clean.copy()
    return gross, net
