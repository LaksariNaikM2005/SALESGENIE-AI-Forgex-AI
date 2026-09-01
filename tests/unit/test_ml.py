import pytest
from ai_ml_engine.inference.predict import predict_lead

def test_predict_lead_output_structure():
    sample_lead = {
        "account": "Test Corp",
        "sector": "technolgy",
        "year_established": 2010,
        "revenue": 5000.0,
        "employees": 150,
        "office_location": "United States",
        "subsidiary_of": None,
        "product": "GTX Basic",
        "series": "GTX",
        "sales_price": 500,
        "sales_agent": "Moses Frase",
        "manager": "Unknown",
        "regional_office": "Central",
        "engage_year": 2024,
        "engage_month": 5,
        "engage_quarter": 2,
        "engage_dayofweek": 1,
        "account_age": 14,
        "historical_global_win_rate": 0.50,
        "historical_account_win_rate": 0.50,
        "historical_product_win_rate": 0.50,
        "historical_agent_win_rate": 0.50,
        "historical_sector_win_rate": 0.50,
        "account_previous_deals": 1,
        "product_previous_deals": 2,
        "agent_previous_deals": 5,
    }

    result = predict_lead(sample_lead)

    assert "prediction" in result
    assert "purchase_probability" in result
    assert "lead_score" in result
    assert result["prediction"] in ["Won", "Lost"]
    assert 0.0 <= result["purchase_probability"] <= 1.0
    assert 0.0 <= result["lead_score"] <= 100.0
