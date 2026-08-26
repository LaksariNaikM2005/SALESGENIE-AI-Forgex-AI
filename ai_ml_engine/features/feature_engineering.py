import pandas as pd

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


PROCESSED_DIR = Path(
    "ai_ml_engine/data/processed"
)


CATEGORICAL_FEATURES = [
    "account",
    "sector",
    "office_location",
    "subsidiary_of",
    "product",
    "series",
    "sales_agent",
    "manager",
    "regional_office",
]


NUMERIC_FEATURES = [
    "year_established",
    "revenue",
    "employees",
    "sales_price",
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


def create_preprocessor():

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=True,
                ),
            ),
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
        ]
    )


def load_training_data():

    path = (
        PROCESSED_DIR
        / "training_dataset.csv"
    )

    df = pd.read_csv(path)

    feature_columns = (
        CATEGORICAL_FEATURES
        + NUMERIC_FEATURES
    )

    return (
        df[feature_columns],
        df["target"]
    )


if __name__ == "__main__":

    import pandas as pd

    X, y = load_training_data()

    preprocessor = create_preprocessor()

    X_transformed = (
        preprocessor.fit_transform(X)
    )

    print(
        "Original feature count:",
        X.shape[1]
    )

    print(
        "Transformed feature shape:",
        X_transformed.shape
    )

    print(
        "Feature engineering pipeline OK."
    )