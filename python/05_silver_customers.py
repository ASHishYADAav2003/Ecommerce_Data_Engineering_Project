
from pathlib import Path
import pandas as pd

# 1. Define project and data paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "olist_customers_dataset.csv"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "silver" / "customers"
OUTPUT_FILE = OUTPUT_DIR / "customers.parquet"

# 2. Create output folder if it does not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load the raw customers dataset
customers = pd.read_csv(
    RAW_FILE,
    dtype={"customer_zip_code_prefix": "string"}
)

print("Raw customers dataset loaded.")
print("Rows before cleaning:", len(customers))

# 4. Clean text columns
customers["customer_id"] = customers["customer_id"].str.strip()
customers["customer_unique_id"] = customers["customer_unique_id"].str.strip()

customers["customer_city"] = customers["customer_city"].str.strip()
customers["customer_state"] = customers["customer_state"].str.strip().str.upper()

# 5. Validate required customer IDs
if customers["customer_id"].isnull().any():
    raise ValueError("Missing customer_id values found!")

if customers["customer_id"].duplicated().any():
    raise ValueError("Duplicate customer_id values found!")

# 6. Check missing values
print("\nMissing values after cleaning:")
print(customers.isnull().sum())

# 7. Save the cleaned dataset as Parquet
customers.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Customers dataset created successfully!")
print("Rows after cleaning:", len(customers))
print("Columns:", customers.columns.tolist())
print("Output file:", OUTPUT_FILE)
