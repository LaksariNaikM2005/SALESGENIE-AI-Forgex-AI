import logging
from pathlib import Path
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = PROJECT_ROOT / "ai_ml_engine" / "data" / "processed"


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


def create_preprocessor() -> ColumnTransformer:
    """
    Creates a scikit-learn ColumnTransformer pipeline that handles missing values,
    scales numerical features, and one-hot encodes categorical features.
    """
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
        ]
    )


def load_training_data() -> tuple[pd.DataFrame, pd.Series]:
    """
    Loads feature matrix X and target vector y from the processed dataset.
    """
    path = PROCESSED_DIR / "training_dataset.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"Processed dataset file not found: {path}. Please run preprocessor module first."
        )

    df = pd.read_csv(path)
    feature_columns = CATEGORICAL_FEATURES + NUMERIC_FEATURES

    X = df[feature_columns]
    y = df["target"]

    return X, y


if __name__ == "__main__":
    X, y = load_training_data()
    preprocessor = create_preprocessor()
    X_transformed = preprocessor.fit_transform(X)
    print("Feature Engineering Check:")
    print("Original Feature Count:", X.shape[1])
    print("Transformed Feature Shape:", X_transformed.shape)
    print("Target Shape:", y.shape)