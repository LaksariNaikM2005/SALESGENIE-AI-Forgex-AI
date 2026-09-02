import os
import pandas as pd

RAW_DIR = "ai_ml_engine/data/raw"
PROCESSED_DIR = "ai_ml_engine/data/processed"

# 1. Delete manufacturing_sector_dataset.csv
mfg_file = os.path.join(RAW_DIR, "manufacturing_sector_dataset.csv")
if os.path.exists(mfg_file):
    os.remove(mfg_file)
    print(f"Deleted: {mfg_file}")

# 2. Delete training_dataset.csv
processed_file = os.path.join(PROCESSED_DIR, "training_dataset.csv")
if os.path.exists(processed_file):
    os.remove(processed_file)
    print(f"Deleted: {processed_file}")

# 3. Revert accounts.csv to default (remove manufacturing entries)
accounts_file = os.path.join(RAW_DIR, "accounts.csv")
if os.path.exists(accounts_file):
    acc_df = pd.read_csv(accounts_file)
    original_acc_df = acc_df[~acc_df["sector"].str.contains("manufacturing|heavy_equipment|machinery|semiconductor|tooling|chemical", case=False, na=False)]
    original_acc_df.to_csv(accounts_file, index=False)
    print(f"Reverted {accounts_file} to original {len(original_acc_df)} accounts.")

# 4. Revert products.csv to default
products_file = os.path.join(RAW_DIR, "products.csv")
if os.path.exists(products_file):
    prod_df = pd.read_csv(products_file)
    original_prods = ["GTX Basic", "GTX Pro", "MG Special", "MG Advanced", "GTX Plus Pro", "GTX Plus Basic", "GTK 500"]
    original_prod_df = prod_df[prod_df["product"].isin(original_prods)]
    original_prod_df.to_csv(products_file, index=False)
    print(f"Reverted {products_file} to original {len(original_prod_df)} products.")
