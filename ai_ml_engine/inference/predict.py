import logging
from pathlib import Path
import warnings
import joblib
import pandas as pd

from ai_ml_engine.features.feature_engineering import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
)

# Suppress sklearn unpickle version mismatch warnings cleanly
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*unpickle estimator.*")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = PROJECT_ROOT / "ai_ml_engine" / "models" / "lead_scoring_model.joblib"

FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def load_model():
    """Loads the persisted scikit-learn pipeline model cleanly without version warnings."""
    if not MODEL_PATH.exists():
        logger.warning(f"Trained ML model artifact not found at: {MODEL_PATH}")
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return joblib.load(MODEL_PATH)


def predict_lead(lead_data: dict) -> dict:
    """
    Accepts raw lead attribute dict, transforms inputs, runs inference,
    and returns lead score, purchase probability, and prediction class.
    """
    model = load_model()

    df = pd.DataFrame([lead_data])

    # Ensure all expected feature columns exist
    for column in FEATURE_COLUMNS:
        if column not in df.columns or pd.isna(df[column].iloc[0]):
            if column in NUMERIC_FEATURES:
                df[column] = 0.0
            else:
                df[column] = "Unknown"

    df = df[FEATURE_COLUMNS]

    if model is None:
        base_prob = pd.to_numeric(
            lead_data.get("historical_global_win_rate", 0.5), errors="coerce"
        )
        purchase_prob = float(0.5 if pd.isna(base_prob) else max(0.0, min(1.0, base_prob)))
    else:
        try:
            probabilities = model.predict_proba(df)[0]
            purchase_prob = float(probabilities[1])
        except Exception:
            prediction_val = int(model.predict(df)[0])
            purchase_prob = 1.0 if prediction_val == 1 else 0.0

    prediction_class = "Won" if purchase_prob >= 0.10 else "Lost"
    # Calibrate model probability (0.0 - 0.20+) into 0 - 100 score scale
    if purchase_prob <= 0.20:
        lead_score = min(100.0, round((purchase_prob / 0.20) * 100.0, 2))
    else:
        lead_score = min(100.0, round(purchase_prob * 100.0, 2))

    # Lead temperature range: Hot (>=82), Warm (>=45), Cold (<45)
    if lead_score >= 82.0:
        lead_temperature = "Hot Lead"
    elif lead_score >= 45.0:
        lead_temperature = "Warm Lead"
    else:
        lead_temperature = "Cold Lead"

    # Stage mapping range: Won (>=75), Negotiation (>=70), Proposal (>=50), Qualified (>=25), New Lead (<=25)
    if lead_score >= 75.0:
        recommended_stage = "Won"
    elif lead_score >= 70.0:
        recommended_stage = "Negotiation"
    elif lead_score >= 50.0:
        recommended_stage = "Proposal"
    elif lead_score >= 25.0:
        recommended_stage = "Qualified"
    else:
        recommended_stage = "New Lead"

    return {
        "prediction": prediction_class,
        "purchase_probability": round(purchase_prob, 4),
        "lead_score": lead_score,
        "lead_temperature": lead_temperature,
        "recommended_stage": recommended_stage,
    }


if __name__ == "__main__":
    print("Testing Model Reload & Inference...")
    sample_lead = {
        "account": "Apex Precision Robotics",
        "sector": "industrial_automation",
        "year_established": 1998,
        "revenue": 85.0,
        "employees": 1450,
        "office_location": "United States",
        "subsidiary_of": "Apex Global",
        "product": "Robotic Assembly Cell X7",
        "series": "Industrial Automation",
        "sales_price": 125000,
        "sales_agent": "Marcus Vance",
        "manager": "Alex Vance",
        "regional_office": "Midwest Region",
        "engage_year": 2024,
        "engage_month": 5,
        "engage_quarter": 2,
        "engage_dayofweek": 3,
        "account_age": 26,
        "deal_cycle_days": 45,
        "price_ratio": 1.1,
        "revenue_per_employee": 0.0586,
        "historical_global_win_rate": 0.54,
        "historical_account_win_rate": 0.60,
        "historical_product_win_rate": 0.58,
        "historical_agent_win_rate": 0.55,
        "historical_sector_win_rate": 0.56,
        "account_previous_deals": 3,
        "product_previous_deals": 10,
        "agent_previous_deals": 15,
    }

    result = predict_lead(sample_lead)
    print("Inference Result:", result)