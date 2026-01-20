"""K-means clustering utilities."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


@dataclass
class KMeansDiagnostics:
    """Container for K-means diagnostics."""
    inertia: dict
    silhouette: dict


def run_kmeans(
    customer_df: pd.DataFrame,
    features: list[str] | None = None,
    k_range: range = range(2, 11),
) -> tuple[KMeans, pd.DataFrame, KMeansDiagnostics]:
    """Run K-means clustering and return model, labeled data, and diagnostics."""
    if features is None:
        features = ["recency_days", "frequency", "monetary"]

    df = customer_df.copy()
    df["monetary_log"] = np.log1p(df["monetary"])
    df["frequency_log"] = np.log1p(df["frequency"])

    if "monetary" in features:
        features = [f if f != "monetary" else "monetary_log" for f in features]
    if "frequency" in features:
        features = [f if f != "frequency" else "frequency_log" for f in features]

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[features])

    inertia = {}
    silhouette = {}
    models = {}

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(scaled)
        inertia[k] = model.inertia_
        try:
            silhouette[k] = silhouette_score(scaled, labels)
        except ValueError:
            # Silhouette score fails if dataset is too small (n_samples < k)
            silhouette[k] = np.nan
        models[k] = model

    best_k = max(silhouette, key=silhouette.get)
    best_model = models[best_k]
    df["cluster"] = best_model.predict(scaled)

    diagnostics = KMeansDiagnostics(inertia=inertia, silhouette=silhouette)
    return best_model, df, diagnostics


def summarize_clusters(labeled_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize cluster profiles for interpretation."""
    summary = (
        labeled_df.groupby("cluster")
        .agg(
            customers=("CustomerID", "count"),
            revenue=("monetary", "sum"),
            avg_recency=("recency_days", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
        )
        .reset_index()
    )
    summary["pct_customers"] = summary["customers"] / summary["customers"].sum()
    summary["revenue_share"] = summary["revenue"] / summary["revenue"].sum()
    return summary
