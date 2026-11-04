
from pathlib import Path
import pandas as pd

# 1. Define project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

GOLD_DIR = PROJECT_DIR / "data" / "gold"

# 2. Define Gold datasets and their unique keys
datasets = {
    "Gold Orders": {
        "file": "gold_orders/gold_orders.parquet",
        "keys": ["order_id"]
    },
    "Gold Revenue": {
        "file": "gold_revenue/gold_revenue.parquet",
        "keys": ["order_id", "order_item_id"]
    },
    "Gold Customers": {
        "file": "gold_customers/gold_customers.parquet",
        "keys": ["customer_id"]
    },
    "Gold Products": {
        "file": "gold_products/gold_products.parquet",
        "keys": ["product_id"]
    },
    "Gold Sellers": {
        "file": "gold_sellers/gold_sellers.parquet",
        "keys": ["seller_id"]
    },
    "Gold Reviews": {
        "file": "gold_reviews/gold_reviews.parquet",
        "keys": ["review_id", "order_id"]
    }
}

# 3. Initialize counters
successful = 0
failed = 0

print("=" * 70)
print("GOLD LAYER VALIDATION REPORT")
print("=" * 70)

# 4. Validate every Gold dataset
for dataset_name, details in datasets.items():

    file_path = GOLD_DIR / details["file"]
    keys = details["keys"]

    print(f"\nDataset: {dataset_name}")
    print("-" * 50)

    if not file_path.exists():
        print("FAILED: File not found")
        failed += 1
        continue

    try:
        # Read the Parquet dataset
        df = pd.read_parquet(file_path)

        # Check required key columns exist
        missing_columns = [
            column for column in keys
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing key columns: {missing_columns}"
            )

        # Check missing key values
        missing_keys = df[keys].isnull().any(axis=1).sum()

        # Check duplicate keys
        duplicate_keys = df.duplicated(
            subset=keys
        ).sum()

        print("Rows:", len(df))
        print("Columns:", len(df.columns))
        print("Missing key records:", missing_keys)
        print("Duplicate key records:", duplicate_keys)

        # Mark dataset as successful only if key checks pass
        if missing_keys == 0 and duplicate_keys == 0:
            print("Status: SUCCESS")
            successful += 1
        else:
            print("Status: FAILED - Key validation issue")
            failed += 1

    except Exception as error:
        print("Status: FAILED")
        print("Error:", error)
        failed += 1

# 5. Final validation summary
print("\n" + "=" * 70)
print("FINAL GOLD VALIDATION SUMMARY")
print("=" * 70)

print("Total datasets:", len(datasets))
print("Successful datasets:", successful)
print("Failed datasets:", failed)

if failed == 0:
    print("\nALL GOLD DATASETS PASSED VALIDATION!")
else:
    print("\nSOME GOLD DATASETS NEED ATTENTION.")
