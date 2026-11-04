
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "olist_orders_dataset.csv"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "silver" / "orders"
OUTPUT_FILE = OUTPUT_DIR / "orders.parquet"

# 2. Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load raw orders dataset
orders = pd.read_csv(RAW_FILE)

print("Raw orders dataset loaded.")
print("Rows before cleaning:", len(orders))

# 4. Standardize order status
orders["order_status"] = orders["order_status"].str.strip().str.lower()

# 5. Convert timestamp columns to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

# 6. Validate required identifiers
if orders["order_id"].isnull().any():
    raise ValueError("Missing order_id values found!")

if orders["order_id"].duplicated().any():
    raise ValueError("Duplicate order_id values found!")

# 7. Display missing values
print("\nMissing values after cleaning:")
print(orders.isnull().sum())

# 8. Save as Parquet
orders.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Orders dataset created successfully!")
print("Rows after cleaning:", len(orders))
print("Output file:", OUTPUT_FILE)
print("\nData types after cleaning:")
print(orders.dtypes)
