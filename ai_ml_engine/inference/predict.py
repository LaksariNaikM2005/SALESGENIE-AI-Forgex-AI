from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path(
    "ai_ml_engine/models/lead_scoring_model.joblib"
)


FEATURE_COLUMNS = [
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


def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(
        MODEL_PATH
    )


def predict_lead(lead_data):

    model = load_model()

    df = pd.DataFrame(
        [lead_data]
    )

    # Ensure every expected feature exists.
    for column in FEATURE_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[
        FEATURE_COLUMNS
    ]

    probability = float(
        model.predict_proba(
            df
        )[0][1]
    )

    prediction = int(
        model.predict(df)[0]
    )

    lead_score = round(
        probability * 100,
        2
    )

    return {
        "prediction": (
            "Won"
            if prediction == 1
            else "Lost"
        ),
        "purchase_probability": round(
            probability,
            4
        ),
        "lead_score": lead_score,
    }


if __name__ == "__main__":

    example = {
        "account": "Acme Corporation",
        "sector": "technolgy",
        "year_established": 1996,
        "revenue": 1100.04,
        "employees": 2822,
        "office_location": "United States",
        "subsidiary_of": None,
        "product": "GTX Basic",
        "series": "GTX",
        "sales_price": 550,
        "sales_agent": "Moses Frase",
        "manager": "Unknown",
        "regional_office": "Central",
        "engage_year": 2017,
        "engage_month": 1,
        "engage_quarter": 1,
        "engage_dayofweek": 2,
        "account_age": 21,

        "historical_global_win_rate": 0.50,
        "historical_account_win_rate": 0.50,
        "historical_product_win_rate": 0.50,
        "historical_agent_win_rate": 0.50,
        "historical_sector_win_rate": 0.50,

        "account_previous_deals": 0,
        "product_previous_deals": 0,
        "agent_previous_deals": 0,
    }

    print(
        predict_lead(example)
    )