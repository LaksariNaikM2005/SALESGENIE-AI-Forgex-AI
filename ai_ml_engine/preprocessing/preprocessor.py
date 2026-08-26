from pathlib import Path

import pandas as pd


RAW_DIR = Path("ai_ml_engine/data/raw")
PROCESSED_DIR = Path("ai_ml_engine/data/processed")


def load_raw_data():
    accounts = pd.read_csv(RAW_DIR / "accounts.csv")
    products = pd.read_csv(RAW_DIR / "products.csv")
    pipeline = pd.read_csv(RAW_DIR / "sales_pipeline.csv")
    sales_teams = pd.read_csv(RAW_DIR / "sales_teams.csv")

    return accounts, products, pipeline, sales_teams


def _normalize(df):
    df = df.copy()
    df.columns = [
        str(c).strip().lower()
        for c in df.columns
    ]
    return df


def _clean_text(df):
    text_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for col in text_columns:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
        )

    return df


def add_temporal_history_features(dataset):
    """
    Calculate historical win rates using ONLY records
    that occurred before the current opportunity.
    """

    dataset = dataset.sort_values(
        "engage_date"
    ).copy()

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

        # Smoothed rates.
        def smoothed(stats):
            wins, total = stats
            return (wins + 5) / (total + 10)

        if global_total > 0:
            dataset.at[
                index,
                "historical_global_win_rate"
            ] = (
                global_wins + 5
            ) / (
                global_total + 10
            )

        if account in account_stats:
            wins, total = account_stats[account]

            dataset.at[
                index,
                "historical_account_win_rate"
            ] = smoothed((wins, total))

            dataset.at[
                index,
                "account_previous_deals"
            ] = total

        if product in product_stats:
            wins, total = product_stats[product]

            dataset.at[
                index,
                "historical_product_win_rate"
            ] = smoothed((wins, total))

            dataset.at[
                index,
                "product_previous_deals"
            ] = total

        if agent in agent_stats:
            wins, total = agent_stats[agent]

            dataset.at[
                index,
                "historical_agent_win_rate"
            ] = smoothed((wins, total))

            dataset.at[
                index,
                "agent_previous_deals"
            ] = total

        if sector in sector_stats:
            wins, total = sector_stats[sector]

            dataset.at[
                index,
                "historical_sector_win_rate"
            ] = smoothed((wins, total))

        # Update statistics AFTER generating current-row features.
        target = int(row["target"])

        global_wins += target
        global_total += 1

        if account:
            wins, total = account_stats.get(
                account,
                (0, 0)
            )
            account_stats[account] = (
                wins + target,
                total + 1
            )

        if product:
            wins, total = product_stats.get(
                product,
                (0, 0)
            )
            product_stats[product] = (
                wins + target,
                total + 1
            )

        if agent:
            wins, total = agent_stats.get(
                agent,
                (0, 0)
            )
            agent_stats[agent] = (
                wins + target,
                total + 1
            )

        if sector:
            wins, total = sector_stats.get(
                sector,
                (0, 0)
            )
            sector_stats[sector] = (
                wins + target,
                total + 1
            )

    return dataset


def build_training_dataset():

    accounts, products, pipeline, sales_teams = (
        load_raw_data()
    )

    accounts = _clean_text(
        _normalize(accounts)
    )

    products = _clean_text(
        _normalize(products)
    )

    pipeline = _clean_text(
        _normalize(pipeline)
    )

    sales_teams = _clean_text(
        _normalize(sales_teams)
    )

    dataset = pipeline[
        pipeline["deal_stage"].isin(
            ["Won", "Lost"]
        )
    ].copy()

    dataset["target"] = (
        dataset["deal_stage"]
        .map({
            "Won": 1,
            "Lost": 0
        })
        .astype(int)
    )

    dataset["engage_date"] = pd.to_datetime(
        dataset["engage_date"],
        errors="coerce"
    )

    dataset = dataset.dropna(
        subset=["engage_date"]
    )

    dataset = dataset.merge(
        accounts,
        on="account",
        how="left"
    )

    dataset = dataset.merge(
        products,
        on="product",
        how="left"
    )

    dataset = dataset.merge(
        sales_teams,
        on="sales_agent",
        how="left"
    )

    dataset["engage_year"] = (
        dataset["engage_date"].dt.year
    )

    dataset["engage_month"] = (
        dataset["engage_date"].dt.month
    )

    dataset["engage_quarter"] = (
        dataset["engage_date"].dt.quarter
    )

    dataset["engage_dayofweek"] = (
        dataset["engage_date"].dt.dayofweek
    )

    dataset["account_age"] = (
        dataset["engage_year"]
        - dataset["year_established"]
    )

    # Historical features.
    dataset = add_temporal_history_features(
        dataset
    )

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

        "historical_global_win_rate",
        "historical_account_win_rate",
        "historical_product_win_rate",
        "historical_agent_win_rate",
        "historical_sector_win_rate",

        "account_previous_deals",
        "product_previous_deals",
        "agent_previous_deals",
    ]

    dataset = dataset[
        feature_columns + ["target"]
    ]

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output = (
        PROCESSED_DIR
        / "training_dataset.csv"
    )

    dataset.to_csv(
        output,
        index=False
    )

    print(
        f"Training dataset saved to: {output}"
    )

    print(
        f"Shape: {dataset.shape}"
    )

    print(
        "\nTarget distribution:"
    )

    print(
        dataset["target"].value_counts()
    )

    return dataset


if __name__ == "__main__":
    build_training_dataset()