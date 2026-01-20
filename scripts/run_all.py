"""Run full customer segmentation pipeline."""
from __future__ import annotations

import pandas as pd

from src import config
from src.cleaning import clean_transactions, split_gross_net
from src.clustering import run_kmeans, summarize_clusters
from src.cohort import build_cohorts, retention_matrix, revenue_matrix
from src.features import make_customer_table
from src.io import load_raw_transactions, save_dataframe
from src.rfm import score_rfm, assign_rfm_segments
from src.viz import set_plot_style, save_fig, barplot_segments, heatmap_table


def main() -> None:
    """Execute the end-to-end workflow."""
    config.ensure_directories()
    set_plot_style()

    print("Loading raw data...")
    raw = load_raw_transactions()

    print("Cleaning transactions...")
    cleaned = clean_transactions(raw)
    gross, net = split_gross_net(cleaned)

    dataset = gross if config.PRIMARY_DATASET == "gross" else net
    missing_customers = dataset["CustomerID"].isna().sum()
    missing_revenue = dataset.loc[dataset["CustomerID"].isna(), "Revenue"].sum()
    if missing_customers:
        print(
            f"Dropping {missing_customers} rows with missing CustomerID "
            f"(revenue impact: {missing_revenue:,.2f})."
        )
    dataset = dataset.dropna(subset=["CustomerID"])

    save_dataframe(cleaned, config.PROCESSED_DIR / "transactions_clean.csv")

    print("Building customer table...")
    customer_table = make_customer_table(dataset)
    save_dataframe(customer_table, config.PROCESSED_DIR / "customer_table.csv")

    print("Scoring RFM...")
    scored = score_rfm(customer_table, n_tiles=config.DEFAULT_N_TILES)
    segmented = assign_rfm_segments(scored)

    segment_summary = (
        segmented.groupby("RFM_SEGMENT")
        .agg(customers=("CustomerID", "count"), revenue=("monetary", "sum"))
        .reset_index()
        .sort_values("customers", ascending=False)
    )
    save_dataframe(segment_summary, config.TABLES_DIR / "rfm_segment_summary.csv")

    print("Saving RFM plots...")
    barplot_segments(segment_summary, "RFM Segment Counts")
    save_fig(config.FIGURES_DIR / "rfm_segment_bar.png")

    pd.plotting.scatter_matrix(
        segmented[["recency_days", "frequency", "monetary"]],
        figsize=(6, 6),
        diagonal="kde",
    )
    save_fig(config.FIGURES_DIR / "rfm_recency_frequency_scatter.png")

    print("Running K-means clustering...")
    model, labeled, diagnostics = run_kmeans(customer_table)
    cluster_summary = summarize_clusters(labeled)
    save_dataframe(cluster_summary, config.TABLES_DIR / "cluster_summary.csv")

    pd.DataFrame({"k": list(diagnostics.inertia.keys()), "inertia": list(diagnostics.inertia.values())}).plot(
        x="k", y="inertia", marker="o", title="Elbow Plot"
    )
    save_fig(config.FIGURES_DIR / "kmeans_elbow.png")

    pd.DataFrame(
        {"k": list(diagnostics.silhouette.keys()), "silhouette": list(diagnostics.silhouette.values())}
    ).plot(x="k", y="silhouette", marker="o", title="Silhouette Scores")
    save_fig(config.FIGURES_DIR / "kmeans_silhouette.png")

    cluster_summary.set_index("cluster")[["avg_recency", "avg_frequency", "avg_monetary"]].plot(
        kind="bar", figsize=(6, 4), title="Cluster Profiles"
    )
    save_fig(config.FIGURES_DIR / "cluster_profiles.png")

    print("Running cohort analysis...")
    cohort_df = build_cohorts(dataset)
    retention = retention_matrix(cohort_df)
    revenue = revenue_matrix(cohort_df)
    save_dataframe(retention.reset_index(), config.TABLES_DIR / "cohort_retention.csv")
    save_dataframe(revenue.reset_index(), config.TABLES_DIR / "cohort_revenue.csv")

    heatmap_table(retention, "Cohort Retention", fmt=".0%")
    save_fig(config.FIGURES_DIR / "cohort_retention_heatmap.png")

    heatmap_table(revenue.fillna(0), "Cohort Revenue", fmt=".0f")
    save_fig(config.FIGURES_DIR / "cohort_revenue_heatmap.png")

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
