
from pathlib import Path
import pandas as pd

# Project directory and raw data folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"

# All 9 Olist CSV files
csv_files = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]

print("=" * 70)
print("OLIST E-COMMERCE DATA EXPLORATION")
print("=" * 70)

for file_name in csv_files:
    file_path = RAW_DATA_DIR / file_name

    print(f"\n\n{'=' * 70}")
    print(f"FILE: {file_name}")
    print("=" * 70)

    if not file_path.exists():
        print("ERROR: File not found!")
        continue

    try:
        df = pd.read_csv(file_path)

        print(f"Number of rows: {df.shape[0]}")
        print(f"Number of columns: {df.shape[1]}")

        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nData types:")
        print(df.dtypes)

        print("\nMissing values:")
        print(df.isnull().sum())

        print("\nFirst 5 records:")
        print(df.head())

    except Exception as error:
        print(f"Error reading file: {error}")

print("\n\nExploration completed!")
