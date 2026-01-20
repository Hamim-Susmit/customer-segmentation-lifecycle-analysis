"""Feature engineering utilities."""
from __future__ import annotations

from datetime import timedelta
import pandas as pd


def make_customer_table(df_clean: pd.DataFrame, snapshot_date: pd.Timestamp | None = None) -> pd.DataFrame:
    """Build a customer-level feature table with RFM metrics."""
    df = df_clean.copy()
    df = df.dropna(subset=["CustomerID"])

    if snapshot_date is None:
        snapshot_date = df["InvoiceDate"].max() + timedelta(days=1)

    customer = (
        df.groupby("CustomerID")
        .agg(
            last_purchase_date=("InvoiceDate", "max"),
            first_purchase_date=("InvoiceDate", "min"),
            frequency=("Invoice", "nunique"),
            monetary=("Revenue", "sum"),
        )
        .reset_index()
    )

    customer["recency_days"] = (snapshot_date - customer["last_purchase_date"]).dt.days
    customer["tenure_days"] = (snapshot_date - customer["first_purchase_date"]).dt.days
    customer["aov"] = customer["monetary"] / customer["frequency"]
    customer["snapshot_date"] = snapshot_date

    return customer
