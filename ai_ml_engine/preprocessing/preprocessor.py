import logging
from pathlib import Path
import pandas as pd

from ai_ml_engine.preprocessing.data_loader import load_all_raw_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = PROJECT_ROOT / "ai_ml_engine" / "data" / "processed"


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df


def _clean_text(df: pd.DataFrame) -> pd.DataFrame:
    text_columns = df.select_dtypes(include=["object"]).columns
    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()
    return df


def add_temporal_history_features(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates historical win rates chronologically using ONLY records
    that occurred before the current opportunity to prevent temporal target leakage.
    """
    dataset["engage_date_dt"] = pd.to_datetime(dataset["engage_date"], errors="coerce")
    dataset = dataset.sort_values("engage_date_dt").reset_index(drop=True)

    dataset["historical_global_win_rate"] = 0.5
    dataset["historical_account_win_rate"] = 0.5
    dataset["historical_product_win_rate"] = 0.5
    dataset["historical_agent_win_rate"] = 0.5
    dataset["historical_sector_win_rate"] = 0.5

    dataset["account_previous_deals"] = 0
    dataset["product_previous_deals"] = 0
    dataset["agent_previous_deals"] = 0

    global_wins = 0
    global_total = 0

    account_stats = {}
    product_stats = {}
    agent_stats = {}
    sector_stats = {}

    for index, row in dataset.iterrows():
        account = row.get("account")
        product = row.get("product")
        agent = row.get("sales_agent")
        sector = row.get("sector")

        def smoothed(stats):
            wins, total = stats
            return (wins + 5) / (total + 10)

        if global_total > 0:
            dataset.at[index, "historical_global_win_rate"] = (global_wins + 5) / (
                global_total + 10
            )

        if account in account_stats:
            wins, total = account_stats[account]
            dataset.at[index, "historical_account_win_rate"] = smoothed((wins, total))
            dataset.at[index, "account_previous_deals"] = total

        if product in product_stats:
            wins, total = product_stats[product]
            dataset.at[index, "historical_product_win_rate"] = smoothed((wins, total))
            dataset.at[index, "product_previous_deals"] = total

        if agent in agent_stats:
            wins, total = agent_stats[agent]
            dataset.at[index, "historical_agent_win_rate"] = smoothed((wins, total))
            dataset.at[index, "agent_previous_deals"] = total

        if sector in sector_stats:
            wins, total = sector_stats[sector]
            dataset.at[index, "historical_sector_win_rate"] = smoothed((wins, total))

        target = int(row["target"])
        global_wins += target
        global_total += 1

        if account:
            wins, total = account_stats.get(account, (0, 0))
            account_stats[account] = (wins + target, total + 1)

        if product:
            wins, total = product_stats.get(product, (0, 0))
            product_stats[product] = (wins + target, total + 1)

        if agent:
            wins, total = agent_stats.get(agent, (0, 0))
            agent_stats[agent] = (wins + target, total + 1)

        if sector:
            wins, total = sector_stats.get(sector, (0, 0))
            sector_stats[sector] = (wins + target, total + 1)

    return dataset


def build_training_dataset() -> pd.DataFrame:
    """
    Builds the clean processed dataset from raw real-world dataset files.
    """
    raw_data = load_all_raw_data()
    accounts = _clean_text(_normalize(raw_data["accounts"]))
    products = _clean_text(_normalize(raw_data["products"]))
    pipeline = _clean_text(_normalize(raw_data["sales_pipeline"]))
    sales_teams = _clean_text(_normalize(raw_data["sales_teams"]))

    dataset = pipeline[pipeline["deal_stage"].isin(["Won", "Lost"])].copy()

    dataset["target"] = dataset["deal_stage"].map({"Won": 1, "Lost": 0}).astype(int)

    dataset["engage_date_dt"] = pd.to_datetime(dataset["engage_date"], errors="coerce")
    dataset["close_date_dt"] = pd.to_datetime(dataset["close_date"], errors="coerce")

    dataset = dataset.dropna(subset=["engage_date_dt"])

    # Engineered domain features
    dataset["deal_cycle_days"] = (dataset["close_date_dt"] - dataset["engage_date_dt"]).dt.days
    dataset["deal_cycle_days"] = dataset["deal_cycle_days"].fillna(30).clip(lower=1)
    dataset["price_ratio"] = (dataset["deal_value"] / (dataset["sales_price"] + 1e-5)).round(4)
    dataset["revenue_per_employee"] = (dataset["revenue"] / (dataset["employees"] + 1)).round(4)

    dataset["engage_year"] = dataset["engage_date_dt"].dt.year
    dataset["engage_month"] = dataset["engage_date_dt"].dt.month
    dataset["engage_quarter"] = dataset["engage_date_dt"].dt.quarter
    dataset["engage_dayofweek"] = dataset["engage_date_dt"].dt.dayofweek

    dataset["account_age"] = dataset["engage_year"] - dataset["year_established"]

    # Historical lag features
    dataset = add_temporal_history_features(dataset)

    feature_columns = [
        "account",
        "sector",
        "year_established",
        "revenue",
        "employees",
        "office_location",
        "subsidiary_of",
        "product",
        "series",
        "sales_price",
        "sales_agent",
        "manager",
        "regional_office",
        "engage_year",
        "engage_month",
        "engage_quarter",
        "engage_dayofweek",
        "account_age",
        "deal_cycle_days",
        "price_ratio",
        "revenue_per_employee",
        "historical_global_win_rate",
        "historical_account_win_rate",
        "historical_product_win_rate",
        "historical_agent_win_rate",
        "historical_sector_win_rate",
        "account_previous_deals",
        "product_previous_deals",
        "agent_previous_deals",
    ]

    final_df = dataset[feature_columns + ["target"]].copy()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DIR / "training_dataset.csv"
    final_df.to_csv(output_file, index=False)

    logger.info(f"Processed training dataset saved to: {output_file}")
    logger.info(f"Final shape: {final_df.shape}")
    logger.info(f"Target distribution:\n{final_df['target'].value_counts()}")

    return final_df


if __name__ == "__main__":
    build_training_dataset()