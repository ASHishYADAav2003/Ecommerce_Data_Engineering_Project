
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "olist_sellers_dataset.csv"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "silver" / "sellers"
OUTPUT_FILE = OUTPUT_DIR / "sellers.parquet"

# 2. Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load raw sellers dataset
sellers = pd.read_csv(
    RAW_FILE,
    dtype={"seller_zip_code_prefix": "string"}
)

print("Raw sellers dataset loaded.")
print("Rows before cleaning:", len(sellers))

# 4. Clean identifier and location columns
sellers["seller_id"] = sellers["seller_id"].str.strip()

sellers["seller_city"] = sellers["seller_city"].str.strip()
sellers["seller_state"] = (
    sellers["seller_state"].str.strip().str.upper()
)

# 5. Validate seller IDs
if sellers["seller_id"].isnull().any():
    raise ValueError("Missing seller_id values found!")

if sellers["seller_id"].duplicated().any():
    raise ValueError("Duplicate seller_id values found!")

# 6. Display missing values
print("\nMissing values after cleaning:")
print(sellers.isnull().sum())

# 7. Save as Parquet
sellers.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Sellers dataset created successfully!")
print("Rows after cleaning:", len(sellers))
print("Output file:", OUTPUT_FILE)

print("\nData types after cleaning:")
print(sellers.dtypes)
