"""Convert the Online Retail II XLSX file to CSV."""
from __future__ import annotations

from pathlib import Path
import argparse

import pandas as pd

from src import config


DEFAULT_XLSX = Path("data/raw/online_retail_II.xlsx")
DEFAULT_CSV = config.RAW_DATA_PATH


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Convert Online Retail II XLSX to CSV")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_XLSX,
        help="Path to the input XLSX file (default: data/raw/online_retail_II.xlsx)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_CSV,
        help="Path to the output CSV file (default: data/raw/online_retail_ii.csv)",
    )
    return parser.parse_args()


def main() -> None:
    """Load the XLSX and save it as CSV."""
    args = parse_args()
    if not args.input.exists():
        raise FileNotFoundError(
            f"Input XLSX not found at {args.input}. "
            "Place the file there or pass --input with the correct path."
        )

    df = pd.read_excel(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Saved CSV to {args.output}")


if __name__ == "__main__":
    main()
