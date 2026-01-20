"""Project configuration and default paths."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_CSV = DATA_DIR / "raw" / "online_retail_ii.csv"
RAW_DATA_XLSX = DATA_DIR / "raw" / "online_retail_ii.xlsx"
RAW_DATA_CSV_ALT = DATA_DIR / "raw" / "online_retail_II.csv"
RAW_DATA_XLSX_ALT = DATA_DIR / "raw" / "online_retail_II.xlsx"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"

PRIMARY_DATASET = "gross"  # Use gross (exclude cancellations/returns) for segmentation.
DEFAULT_N_TILES = 5
DEFAULT_K_RANGE = range(2, 11)


def ensure_directories() -> None:
    """Create output directories if they do not exist."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
