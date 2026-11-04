
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "olist_order_payments_dataset.csv"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "silver" / "payments"
OUTPUT_FILE = OUTPUT_DIR / "payments.parquet"

# 2. Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load raw payments dataset
payments = pd.read_csv(RAW_FILE)

print("Raw payments dataset loaded.")
print("Rows before cleaning:", len(payments))

# 4. Clean identifier and category columns
payments["order_id"] = payments["order_id"].str.strip()
payments["payment_type"] = (
    payments["payment_type"].str.strip().str.lower()
)

# 5. Convert payment values to numeric
payments["payment_value"] = pd.to_numeric(
    payments["payment_value"],
    errors="coerce"
)

# 6. Validate required columns
required_columns = [
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_value"
]

for column in required_columns:
    if payments[column].isnull().any():
        raise ValueError(f"Missing values found in {column}!")

# 7. Check duplicate payment keys
if payments.duplicated(
    subset=["order_id", "payment_sequential"]
).any():
    raise ValueError("Duplicate payment keys found!")

# 8. Validate payment values
if (payments["payment_value"] < 0).any():
    raise ValueError("Negative payment values found!")

# 9. Display missing values
print("\nMissing values after cleaning:")
print(payments.isnull().sum())

# 10. Display payment type distribution
print("\nPayment type distribution:")
print(payments["payment_type"].value_counts())

# 11. Save as Parquet
payments.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Payments dataset created successfully!")
print("Rows after cleaning:", len(payments))
print("Output file:", OUTPUT_FILE)

print("\nData types after cleaning:")
print(payments.dtypes)
