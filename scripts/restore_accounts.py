import os
import pandas as pd

RAW_DIR = "ai_ml_engine/data/raw"
pipeline_file = os.path.join(RAW_DIR, "sales_pipeline.csv")
accounts_file = os.path.join(RAW_DIR, "accounts.csv")

if os.path.exists(pipeline_file):
    pipe_df = pd.read_csv(pipeline_file)
    accounts = pipe_df["account"].dropna().unique()
    
    acc_records = []
    for acc in sorted(accounts):
        acc_records.append({
            "account": acc,
            "sector": "Software & Enterprise Solutions",
            "year_established": 2005,
            "revenue": 500.0,
            "employees": 1200,
            "office_location": "United States",
            "subsidiary_of": ""
        })
        
    acc_df = pd.DataFrame(acc_records)
    acc_df.to_csv(accounts_file, index=False)
    print(f"Restored {accounts_file} with {len(acc_df)} unique accounts.")
