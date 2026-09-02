import logging
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Base directory for raw datasets
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "ai_ml_engine" / "data" / "raw"

REQUIRED_DATASETS = {
    "sales_pipeline": {
        "filename": "sales_pipeline.csv",
        "required_columns": [
            "opportunity_id",
            "sales_agent",
            "regional_office",
            "manager",
            "product",
            "series",
            "sales_price",
            "account",
            "sector",
            "year_established",
            "revenue",
            "employees",
            "office_location",
            "deal_stage",
            "engage_date",
            "close_date",
            "deal_value",
            "target",
        ],
    },
    "accounts": {
        "filename": "accounts.csv",
        "required_columns": [
            "account",
            "sector",
            "year_established",
            "revenue",
            "employees",
            "office_location",
        ],
    },
    "products": {
        "filename": "products.csv",
        "required_columns": ["product", "series", "sales_price"],
    },
    "sales_teams": {
        "filename": "sales_teams.csv",
        "required_columns": ["sales_agent", "regional_office", "manager"],
    },
}


def get_raw_data_dir() -> Path:
    """Returns the validated raw data directory path."""
    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(
            f"Authoritative real-world dataset directory not found at: {RAW_DATA_DIR}"
        )
    return RAW_DATA_DIR


def load_dataset(dataset_key: str) -> pd.DataFrame:
    """
    Loads and validates a single raw dataset file by key.
    """
    if dataset_key not in REQUIRED_DATASETS:
        raise KeyError(f"Unknown dataset key: {dataset_key}")

    info = REQUIRED_DATASETS[dataset_key]
    file_path = get_raw_data_dir() / info["filename"]

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required dataset file missing: {file_path}. "
            "Please ensure real-world dataset files are present in ai_ml_engine/data/raw."
        )

    logger.info(f"Loading raw dataset: {file_path.name}")
    df = pd.read_csv(file_path)

    # Validate column contract
    missing_cols = [c for c in info["required_columns"] if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Dataset {info['filename']} is missing required columns: {missing_cols}"
        )

    logger.info(
        f"Successfully loaded {file_path.name}: {len(df)} rows, {len(df.columns)} columns."
    )
    return df


def load_all_raw_data() -> dict[str, pd.DataFrame]:
    """
    Loads and returns all raw real-world dataset DataFrames.
    """
    datasets = {}
    for key in REQUIRED_DATASETS:
        datasets[key] = load_dataset(key)

    logger.info("All real-world dataset files successfully loaded and validated.")
    return datasets


if __name__ == "__main__":
    print("Executing DataLoader validation check...")
    data = load_all_raw_data()
    for name, df in data.items():
        print(f"[{name}] Rows: {len(df)}, Columns: {list(df.columns)}")
