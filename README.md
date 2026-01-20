# Customer Segmentation & Lifecycle Analysis (Online Retail II)

## Project Overview
This project builds a reusable analytics pipeline for **customer segmentation** and **lifecycle analysis** using the Online Retail II dataset. The goal is to help a retail business answer:

- Who are our highest-value customers?
- Which segments are at risk or dormant?
- How does retention and revenue evolve over time by cohort?

The workflow cleans transaction data, engineers customer-level features, applies rule-based **RFM segmentation**, discovers **K-Means clusters**, and performs **cohort retention & revenue analysis**.

## Dataset
**Online Retail II** contains transactional data for a UK-based online retailer. The pipeline expects:

```
data/raw/online_retail_ii.csv
```

If the file is missing, the pipeline stops with a friendly error prompting you to place it there.

## Methods
### 1) Data Cleaning
- Parse `InvoiceDate` to datetime
- Compute `Revenue = Quantity * UnitPrice`
- Remove zero Quantity rows and non-positive UnitPrice
- Mark cancellations/returns (`Invoice` starts with `C` or Quantity < 0)
- **Gross vs Net**:
  - **Gross** excludes cancellations/returns
  - **Net** includes them

**Primary dataset choice:** This project uses **gross transactions** for segmentation to reflect actual purchase behavior without returns noise.

### 2) Feature Engineering (Customer Table)
From the cleaned data we build:
- `recency_days` (days since last purchase)
- `frequency` (unique invoices per customer)
- `monetary` (total revenue)
- `tenure_days` and `aov` (average order value)

### 3) RFM Segmentation
Quantile-based RFM scoring (1–5) with simple segment mapping:
- Champions
- Loyal
- Potential Loyalist
- New
- Promising
- Needs Attention
- At Risk
- Hibernating

### 4) K-Means Clustering
- Log-transform `monetary` and `frequency` to reduce skew
- Standardize features
- Use elbow + silhouette diagnostics for k selection
- Profile clusters by size, revenue share, and average behaviors

### 5) Cohort Analysis
- Cohort = month of first purchase
- Retention and revenue over months since first purchase
- Heatmaps to visualize lifecycle performance

## Key Findings (Example Outcomes)
Replace with exact values after running the pipeline:
- Champions represent ~X% of customers but generate ~Y% of revenue.
- A large share of customers fall into Hibernating/At Risk segments—win-back campaigns recommended.
- Newer cohorts show lower retention by month 3, indicating onboarding gaps.

## Recommendations by Segment
- **Champions/Loyal:** reward with VIP perks and early product access
- **Potential Loyalist:** nurture with targeted offers and recommendations
- **At Risk/Hibernating:** win-back with time-limited discounts
- **New/Promising:** onboarding sequences and product education

## How to Run
1) Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Place the dataset here:

```
data/raw/online_retail_ii.csv
```

3) Run the full pipeline:

```bash
python scripts/run_all.py
```

Outputs are saved to:
- `data/processed/`
- `reports/figures/`
- `reports/tables/`

## Repo Structure
```
.
├── data/
│   ├── raw/                # place raw CSV here
│   └── processed/          # cleaned data outputs
├── notebooks/              # analysis notebooks
├── reports/
│   ├── figures/            # plots
│   └── tables/             # summary tables
├── scripts/
│   └── run_all.py           # pipeline runner
└── src/                    # modular pipeline code
```

## Limitations & Next Steps
- RFM and K-Means are descriptive; consider A/B testing segment actions.
- Seasonality not explicitly modeled—add holiday flags for stronger insights.
- Explore CLV modeling for long-term value predictions.

---
**Tools:** Python 3.10+, pandas, numpy, matplotlib, seaborn, scikit-learn
