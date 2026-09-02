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

# Output paths
RAW_DIR = "ai_ml_engine/data/raw"

os.makedirs(RAW_DIR, exist_ok=True)

MANUFACTURING_COMPANIES = [
    ("Apex Precision Robotics", "industrial_automation", 1998, 85000000.0, 1450, "United States", "Apex Global"),
    ("Titan Industrial Heavy Machinery", "heavy_equipment", 1985, 240000000.0, 3800, "Germany", ""),
    ("Vanguard CNC Machining Systems", "machinery", 2004, 45000000.0, 620, "Japan", ""),
    ("Starlight Semiconductor Fab", "semiconductor_manufacturing", 2010, 520000000.0, 8500, "Taiwan", ""),
    ("Magna Auto Components", "automotive_manufacturing", 1992, 180000000.0, 2900, "United States", ""),
    ("Precision Die & Mold Works", "tooling_manufacturing", 2001, 28000000.0, 310, "Germany", ""),
    ("Nordic Hydro Chemical Processing", "chemical_manufacturing", 1989, 140000000.0, 1950, "Sweden", ""),
    ("OmniFoundry Materials Group", "metals_manufacturing", 1978, 310000000.0, 4200, "United States", ""),
    ("Bharat Heavy Industrial Equipment", "heavy_equipment", 1995, 95000000.0, 1800, "India", ""),
    ("Kuroda Robotics & Vision", "industrial_automation", 2007, 115000000.0, 1600, "Japan", "Kuroda Group"),
    ("Aerotech Component Systems", "aerospace_manufacturing", 2003, 165000000.0, 2100, "United States", ""),
    ("BioMat Industrial Polymers", "chemical_manufacturing", 2015, 38000000.0, 450, "Germany", ""),
    ("Siemens Smart Factory Solutions", "industrial_automation", 1982, 950000000.0, 14000, "Germany", ""),
    ("Daewoo Precision Motors", "automotive_manufacturing", 1996, 210000000.0, 3400, "South Korea", ""),
    ("Monterrey Industrial Metalworks", "metals_manufacturing", 2008, 62000000.0, 880, "Mexico", ""),
]

MANUFACTURING_PRODUCTS = [
    ("Robotic Assembly Cell X7", "Industrial Automation", 125000),
    ("5-Axis CNC Milling Center", "CNC Machining", 85000),
    ("Industrial IoT Sensor Suite", "Smart Factory", 35000),
    ("Automated Conveyor & Logistics System", "Material Handling", 65000),
    ("AI Quality Vision Inspection System", "QA/QC Inspection", 45000),
    ("Cleanroom Environmental Controller", "Semiconductor Equipment", 150000),
    ("Heavy Duty Hydraulic Press 500T", "Heavy Machinery", 210000),
    ("Laser Cutting & Welding Subsystem", "Precision Tooling", 95000),
]

SALES_AGENTS = [
    ("Marcus Vance", "Midwest Region", "Alex Vance"),
    ("Elena Rostova", "European Operations", "Klaus Weber"),
    ("Kenji Sato", "Asia-Pacific Region", "Takashi Tanaka"),
    ("Sarah Connor", "Americas East", "Alex Vance"),
    ("Rajesh Kumar", "India & SEA Region", "Priya Sharma"),
]

def generate_manufacturing_dataset(num_records=5000):
    print(f"Generating Pure Manufacturing Sector B2B Dataset ({num_records} records)...")
    
    random.seed(42)
    records = []
    
    start_date = datetime(2022, 1, 1)
    
    for i in range(1, num_records + 1):
        company_info = random.choice(MANUFACTURING_COMPANIES)
        product_info = random.choice(MANUFACTURING_PRODUCTS)
        agent_info = random.choice(SALES_AGENTS)
        
        engage_date = start_date + timedelta(days=random.randint(0, 1000))
        
        base_price = product_info[2]
        deal_value = round(base_price * random.uniform(0.9, 1.4), 2)
        
        win_prob = 0.5 + (company_info[3] / 1e9) * 0.2 + random.uniform(-0.25, 0.25)
        win_prob = max(0.1, min(0.95, win_prob))
        
        target = 1 if random.random() < win_prob else 0
        deal_stage = "Won" if target == 1 else "Lost"
        
        record = {
            "opportunity_id": f"MFG-OPP-{i:05d}",
            "sales_agent": agent_info[0],
            "regional_office": agent_info[1],
            "manager": agent_info[2],
            "product": product_info[0],
            "series": product_info[1],
            "sales_price": product_info[2],
            "account": company_info[0],
            "sector": company_info[1],
            "year_established": company_info[2],
            "revenue": company_info[3] / 1e6, # in Millions
            "employees": company_info[4],
            "office_location": company_info[5],
            "subsidiary_of": company_info[6],
            "deal_stage": deal_stage,
            "engage_date": engage_date.strftime("%Y-%m-%d"),
            "close_date": (engage_date + timedelta(days=random.randint(14, 90))).strftime("%Y-%m-%d"),
            "deal_value": deal_value,
            "target": target,
        }
        records.append(record)
        
    df = pd.DataFrame(records)
    out_path = os.path.join(RAW_DIR, "manufacturing_sector_dataset.csv")
    df.to_csv(out_path, index=False)
    print(f"Pure Manufacturing dataset saved to: {out_path} ({len(df)} records)")
    
    # Write sales_pipeline.csv with pure manufacturing records
    pipe_path = os.path.join(RAW_DIR, "sales_pipeline.csv")
    df.to_csv(pipe_path, index=False)
    print(f"Overwrote {pipe_path} with pure Manufacturing sector pipeline deals.")

    update_raw_catalogs()
    return df

def update_raw_catalogs():
    # Write accounts.csv with pure Manufacturing Companies ONLY
    accounts_path = os.path.join(RAW_DIR, "accounts.csv")
    acc_rows = []
    for c in MANUFACTURING_COMPANIES:
        acc_rows.append({
            "account": c[0],
            "sector": c[1],
            "year_established": c[2],
            "revenue": c[3] / 1e6,
            "employees": c[4],
            "office_location": c[5],
            "subsidiary_of": c[6],
        })
    acc_df = pd.DataFrame(acc_rows)
    acc_df.to_csv(accounts_path, index=False)
    print(f"Overwrote {accounts_path} with 100% Manufacturing sector accounts ({len(acc_df)} accounts).")

    # Write products.csv with pure Manufacturing Products ONLY
    products_path = os.path.join(RAW_DIR, "products.csv")
    prod_rows = []
    for p in MANUFACTURING_PRODUCTS:
        prod_rows.append({
            "product": p[0],
            "series": p[1],
            "sales_price": p[2],
        })
    prod_df = pd.DataFrame(prod_rows)
    prod_df.to_csv(products_path, index=False)
    print(f"Overwrote {products_path} with 100% Manufacturing products ({len(prod_df)} products).")

    # Write sales_teams.csv
    teams_path = os.path.join(RAW_DIR, "sales_teams.csv")
    teams_rows = []
    for a in SALES_AGENTS:
        teams_rows.append({
            "sales_agent": a[0],
            "regional_office": a[1],
            "manager": a[2],
        })
    teams_df = pd.DataFrame(teams_rows)
    teams_df.to_csv(teams_path, index=False)
    print(f"Overwrote {teams_path} with sales teams data.")

if __name__ == "__main__":
    generate_manufacturing_dataset()
