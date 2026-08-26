from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline

from ai_ml_engine.features.feature_engineering import (
    create_preprocessor,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
)


DATA_PATH = Path(
    "ai_ml_engine/data/processed/training_dataset.csv"
)

MODEL_DIR = Path(
    "ai_ml_engine/models"
)


def evaluate(name, model, X, y):

    predictions = model.predict(X)

    probabilities = (
        model.predict_proba(X)[:, 1]
    )

    print(f"\n===== {name} =====")

    print(
        "Accuracy:",
        round(
            accuracy_score(
                y,
                predictions
            ),
            4
        )
    )

    print(
        "Precision:",
        round(
            precision_score(
                y,
                predictions
            ),
            4
        )
    )

    print(
        "Recall:",
        round(
            recall_score(
                y,
                predictions
            ),
            4
        )
    )

    print(
        "F1:",
        round(
            f1_score(
                y,
                predictions
            ),
            4
        )
    )

    try:
        print(
            "ROC-AUC:",
            round(
                roc_auc_score(
                    y,
                    probabilities
                ),
                4
            )
        )
    except ValueError:
        print("ROC-AUC: unavailable")


def train_model():

    df = pd.read_csv(
        DATA_PATH
    )

    # Restore chronological order.
    # The preprocessing script already created
    # engage_year/month, but sorting by them gives
    # a deterministic chronological ordering.
    df = df.sort_values(
        [
            "engage_year",
            "engage_month",
            "engage_dayofweek"
        ]
    ).reset_index(
        drop=True
    )

    feature_columns = (
        CATEGORICAL_FEATURES
        + NUMERIC_FEATURES
    )

    X = df[feature_columns]
    y = df["target"]

    total = len(df)

    train_end = int(
        total * 0.60
    )

    validation_end = int(
        total * 0.80
    )

    X_train = X.iloc[:train_end]
    y_train = y.iloc[:train_end]

    X_validation = X.iloc[
        train_end:validation_end
    ]

    y_validation = y.iloc[
        train_end:validation_end
    ]

    X_test = X.iloc[
        validation_end:
    ]

    y_test = y.iloc[
        validation_end:
    ]

    print(
        "Train:",
        X_train.shape
    )

    print(
        "Validation:",
        X_validation.shape
    )

    print(
        "Test:",
        X_test.shape
    )

    preprocessor = create_preprocessor()

    model = RandomForestClassifier(
        n_estimators=400,
        max_depth=12,
        min_samples_split=8,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            ),
        ]
    )

    print(
        "\nTraining Random Forest..."
    )

    pipeline.fit(
        X_train,
        y_train
    )

    print(
        "Training completed."
    )

    evaluate(
        "VALIDATION",
        pipeline,
        X_validation,
        y_validation
    )

    evaluate(
        "TEST",
        pipeline,
        X_test,
        y_test
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    model_path = (
        MODEL_DIR
        / "lead_scoring_model.joblib"
    )

    joblib.dump(
        pipeline,
        model_path
    )

    print(
        f"\nModel saved to: {model_path}"
    )


if __name__ == "__main__":
    train_model()