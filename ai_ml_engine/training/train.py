import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn

from sklearn.ensemble import (
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from ai_ml_engine.features.feature_engineering import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    create_preprocessor,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "ai_ml_engine" / "data" / "processed" / "training_dataset.csv"
MODEL_DIR = PROJECT_ROOT / "ai_ml_engine" / "models"
EVAL_DIR = PROJECT_ROOT / "ai_ml_engine" / "evaluation"


def evaluate_model_performance(name: str, model: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict:
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba") else predictions

    acc = float(accuracy_score(y, predictions))
    prec = float(precision_score(y, predictions, zero_division=0))
    rec = float(recall_score(y, predictions, zero_division=0))
    f1 = float(f1_score(y, predictions, zero_division=0))

    try:
        auc = float(roc_auc_score(y, probabilities))
    except ValueError:
        auc = 0.5

    cm = confusion_matrix(y, predictions).tolist()

    metrics = {
        "model_name": name,
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "roc_auc": round(auc, 4),
        "confusion_matrix": cm,
    }

    print(f"\n--- Metrics for {name} ---")
    print(f"Accuracy:  {metrics['accuracy']}")
    print(f"Precision: {metrics['precision']}")
    print(f"Recall:    {metrics['recall']}")
    print(f"F1-Score:  {metrics['f1']}")
    print(f"ROC-AUC:   {metrics['roc_auc']}")

    return metrics


def train_and_evaluate_all():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed training dataset not found at: {DATA_PATH}. Run preprocessor first."
        )

    df = pd.read_csv(DATA_PATH)

    # Sort chronologically by engagement year, month, and dayofweek
    df = df.sort_values(["engage_year", "engage_month", "engage_dayofweek"]).reset_index(drop=True)

    feature_columns = CATEGORICAL_FEATURES + NUMERIC_FEATURES
    X = df[feature_columns]
    y = df["target"]

    total = len(df)
    train_end = int(total * 0.60)
    val_end = int(total * 0.80)

    X_train, y_train = X.iloc[:train_end], y.iloc[:train_end]
    X_val, y_val = X.iloc[train_end:val_end], y.iloc[train_end:val_end]
    X_test, y_test = X.iloc[val_end:], y.iloc[val_end:]

    print("=" * 50)
    print("FORGE_X AI MODEL TRAINING")
    print("=" * 50)
    print("Dataset:\nsales_pipeline.csv, accounts.csv, products.csv, sales_teams.csv")
    print(f"\nRows:\n{total}")
    print(f"\nFeatures:\n{len(feature_columns)}")
    print("\nTarget:\ntarget (1 = Won, 0 = Lost)")
    print(f"\nTrain:\n{len(X_train)}")
    print(f"\nValidation:\n{len(X_val)}")
    print(f"\nTest:\n{len(X_test)}")
    print("=" * 50)

    # Define Candidate Models
    candidate_configs = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "DecisionTree": DecisionTreeClassifier(max_depth=8, random_state=42),
        "RandomForest": RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_split=6,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
        "GradientBoosting": GradientBoostingClassifier(
            n_estimators=200, learning_rate=0.05, max_depth=5, random_state=42
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=200, learning_rate=0.05, max_depth=6, random_state=42
        ),
    }

    results = []
    trained_pipelines = {}

    for name, clf in candidate_configs.items():
        print(f"\nTraining model candidate: {name}...")
        preprocessor = create_preprocessor()
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", clf)])

        pipeline.fit(X_train, y_train)
        val_metrics = evaluate_model_performance(f"{name} (Val)", pipeline, X_val, y_val)
        val_metrics["pipeline"] = pipeline
        results.append(val_metrics)
        trained_pipelines[name] = pipeline

    # Select best model based on F1-Score & ROC-AUC on Validation set
    results.sort(key=lambda r: (r["f1"], r["roc_auc"], r["accuracy"]), reverse=True)
    best_res = results[0]
    best_name = best_res["model_name"].replace(" (Val)", "")
    best_pipeline = best_res["pipeline"]

    print("\n" + "=" * 50)
    print(f"BEST MODEL SELECTED FOR PRODUCTION: {best_name}")
    print("=" * 50)

    # Evaluate Final Model on Untouched Test Set
    print("\nExecuting Final Test Evaluation on Untouched Test Set...")
    test_metrics = evaluate_model_performance(f"{best_name} (FINAL TEST)", best_pipeline, X_test, y_test)

    # Save Model Artifacts
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    EVAL_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODEL_DIR / "lead_scoring_model.joblib"
    joblib.dump(best_pipeline, model_path)
    print(f"\nSaved production model pipeline to: {model_path}")

    # Metadata
    metadata = {
        "model_name": best_name,
        "model_version": "2.0.0",
        "training_dataset_reference": "ai_ml_engine/data/raw/sales_pipeline.csv",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "total_rows": total,
        "train_rows": len(X_train),
        "validation_rows": len(X_val),
        "test_rows": len(X_test),
        "features": feature_columns,
        "target": "target",
        "validation_metrics": {k: v for k, v in best_res.items() if k != "pipeline"},
        "test_metrics": test_metrics,
        "python_version": f"{sklearn.__file__}",
        "scikit_learn_version": sklearn.__version__,
    }

    metadata_path = MODEL_DIR / "model_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved model metadata to: {metadata_path}")

    # Save Evaluation Report
    eval_metrics_path = EVAL_DIR / "metrics.json"
    eval_summary = {
        "candidates_comparison": [
            {k: v for k, v in r.items() if k != "pipeline"} for r in results
        ],
        "final_selected_model": best_name,
        "final_test_metrics": test_metrics,
    }
    with open(eval_metrics_path, "w", encoding="utf-8") as f:
        json.dump(eval_summary, f, indent=2)
    print(f"Saved metrics summary to: {eval_metrics_path}")

    return best_pipeline, metadata


if __name__ == "__main__":
    train_and_evaluate_all()