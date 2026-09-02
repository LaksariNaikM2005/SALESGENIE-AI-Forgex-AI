"""
DEPRECATED / DISALLOWED FOR MODEL TRAINING:
This script was previously used to generate synthetic dataset records for development.
Production model training MUST use the real-world dataset present in `ai_ml_engine/data/raw`.
Do NOT run this script during production or automated training pipelines.
"""

import os
import random
import pandas as pd
from datetime import datetime, timedelta

RAW_DIR = "ai_ml_engine/data/raw"

os.makedirs(RAW_DIR, exist_ok=True)

# 1. Recreate accounts.csv
accounts_data = [
    ("Acme Corporation", "software", 1996, 1100.04, 2822, "United States", ""),
    ("Betasoloin", "medical", 1999, 251.41, 495, "United States", ""),
    ("Betatech", "medical", 1986, 647.18, 1185, "Kenya", ""),
    ("Bioholding", "medical", 2012, 587.34, 1356, "Philipines", ""),
    ("Bioplex", "medical", 1991, 326.82, 1016, "United States", ""),
    ("Blackzim", "retail", 2009, 497.11, 1588, "United States", ""),
    ("Bluth Company", "software", 1993, 1242.32, 3027, "United States", "Acme Corporation"),
    ("Bubba Gump", "software", 2002, 987.39, 2253, "United States", ""),
    ("Cancity", "retail", 2001, 718.62, 2448, "United States", ""),
    ("Cheers", "entertainment", 1993, 4269.9, 6472, "United States", "Massive Dynamic"),
    ("Codehow", "software", 1998, 2714.9, 2641, "United States", "Acme Corporation"),
    ("Condax", "medical", 2017, 4.54, 9, "United States", ""),
    ("Conecom", "software", 2005, 1520.66, 1806, "United States", ""),
]

acc_df = pd.DataFrame(accounts_data, columns=["account", "sector", "year_established", "revenue", "employees", "office_location", "subsidiary_of"])
acc_df.to_csv(os.path.join(RAW_DIR, "accounts.csv"), index=False)
print("Created accounts.csv")

# 2. Recreate products.csv
products_data = [
    ("GTX Basic", "GTX", 550),
    ("GTX Pro", "GTX", 4821),
    ("MG Special", "MG", 55),
    ("MG Advanced", "MG", 3393),
    ("GTX Plus Pro", "GTX", 5482),
    ("GTX Plus Basic", "GTX", 1096),
    ("GTK 500", "GTK", 26768),
]
prod_df = pd.DataFrame(products_data, columns=["product", "series", "sales_price"])
prod_df.to_csv(os.path.join(RAW_DIR, "products.csv"), index=False)
print("Created products.csv")

# 3. Recreate sales_teams.csv
teams_data = [
    ("Moses Frase", "Unknown", "Central"),
    ("Flavia Fiore", "Unknown", "East"),
    ("Melvin Bardsley", "Unknown", "West"),
    ("Klaus Weber", "Unknown", "Europe"),
]
teams_df = pd.DataFrame(teams_data, columns=["sales_agent", "manager", "regional_office"])
teams_df.to_csv(os.path.join(RAW_DIR, "sales_teams.csv"), index=False)
print("Created sales_teams.csv")

# 4. Recreate sales_pipeline.csv
random.seed(42)
pipeline_records = []
start_date = datetime(2017, 1, 1)

for i in range(1, 1500):
    acc = random.choice(accounts_data)[0]
    prod = random.choice(products_data)
    agent = random.choice(teams_data)[0]
    
    engage_d = start_date + timedelta(days=random.randint(0, 1000))
    target = 1 if random.random() > 0.4 else 0
    stage = "Won" if target == 1 else "Lost"
    
    pipeline_records.append({
        "opportunity_id": f"OPP-{i:05d}",
        "sales_agent": agent,
        "product": prod[0],
        "account": acc,
        "deal_stage": stage,
        "engage_date": engage_d.strftime("%Y-%m-%d"),
        "close_date": (engage_d + timedelta(days=random.randint(10, 60))).strftime("%Y-%m-%d"),
        "close_value": prod[2] * random.uniform(0.8, 1.2),
    })

pipe_df = pd.DataFrame(pipeline_records)
pipe_df.to_csv(os.path.join(RAW_DIR, "sales_pipeline.csv"), index=False)
print(f"Created sales_pipeline.csv ({len(pipe_df)} records)")
