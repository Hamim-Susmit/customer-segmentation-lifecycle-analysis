"""Cohort analysis utilities."""
from __future__ import annotations

import pandas as pd


def build_cohorts(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Assign cohort month and order month to transactions."""
    df = df_clean.copy()
    df = df.dropna(subset=["CustomerID"])
    df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()

    first_purchase = df.groupby("CustomerID")["InvoiceDate"].min().dt.to_period("M").dt.to_timestamp()
    df = df.join(first_purchase, on="CustomerID", rsuffix="_cohort")
    df = df.rename(columns={"InvoiceDate_cohort": "cohort_month"})

    df["cohort_index"] = (
        (df["InvoiceMonth"].dt.year - df["cohort_month"].dt.year) * 12
        + (df["InvoiceMonth"].dt.month - df["cohort_month"].dt.month)
        + 1
    )
    return df


def retention_matrix(cohort_df: pd.DataFrame) -> pd.DataFrame:
    """Build cohort retention matrix as percentages."""
    cohort_counts = cohort_df.groupby(["cohort_month", "cohort_index"])["CustomerID"].nunique().reset_index()
    cohort_pivot = cohort_counts.pivot(index="cohort_month", columns="cohort_index", values="CustomerID")
    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_sizes, axis=0)
    return retention


def revenue_matrix(cohort_df: pd.DataFrame) -> pd.DataFrame:
    """Build cohort revenue matrix."""
    revenue = (
        cohort_df.groupby(["cohort_month", "cohort_index"])["Revenue"].sum().reset_index()
    )
    revenue_pivot = revenue.pivot(index="cohort_month", columns="cohort_index", values="Revenue")
    return revenue_pivot
