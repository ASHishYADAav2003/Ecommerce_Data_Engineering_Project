
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "olist_order_items_dataset.csv"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "silver" / "order_items"
OUTPUT_FILE = OUTPUT_DIR / "order_items.parquet"

# 2. Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load raw order items dataset
items = pd.read_csv(RAW_FILE)

print("Raw order items dataset loaded.")
print("Rows before cleaning:", len(items))

# 4. Clean identifier columns
items["order_id"] = items["order_id"].str.strip()
items["product_id"] = items["product_id"].str.strip()
items["seller_id"] = items["seller_id"].str.strip()

# 5. Convert purchase and shipping dates to datetime
date_columns = [
    "shipping_limit_date"
]

for column in date_columns:
    items[column] = pd.to_datetime(
        items[column],
        errors="coerce"
    )

# 6. Convert price and freight values to numeric
numeric_columns = [
    "price",
    "freight_value"
]

for column in numeric_columns:
    items[column] = pd.to_numeric(
        items[column],
        errors="coerce"
    )

# 7. Validate required identifiers
required_columns = [
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id"
]

for column in required_columns:
    if items[column].isnull().any():
        raise ValueError(f"Missing values found in {column}!")

# 8. Check duplicate order item keys
if items.duplicated(
    subset=["order_id", "order_item_id"]
).any():
    raise ValueError("Duplicate order item keys found!")

# 9. Check for invalid price and freight values
if (items["price"] < 0).any():
    raise ValueError("Negative product prices found!")

if (items["freight_value"] < 0).any():
    raise ValueError("Negative freight values found!")

# 10. Display missing values
print("\nMissing values after cleaning:")
print(items.isnull().sum())

# 11. Save as Parquet
items.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Order Items dataset created successfully!")
print("Rows after cleaning:", len(items))
print("Output file:", OUTPUT_FILE)

print("\nData types after cleaning:")
print(items.dtypes)
