
from pathlib import Path

import pyarrow.parquet as pq

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Define Spark Gold datasets
GOLD_DATASETS = {
    "Gold Orders": {
        "path": PROJECT_DIR / "data" / "gold"
                / "spark_gold_orders" / "gold_orders.parquet",
        "expected_rows": 99441
    },

    "Gold Revenue": {
        "path": PROJECT_DIR / "data" / "gold"
                / "spark_gold_revenue" / "gold_revenue.parquet",
        "expected_rows": 112650
    },

    "Gold Customers": {
        "path": PROJECT_DIR / "data" / "gold"
                / "spark_gold_customers" / "gold_customers.parquet",
        "expected_rows": 99441
    },

    "Gold Products": {
        "path": PROJECT_DIR / "data" / "gold"
                / "spark_gold_products" / "gold_products.parquet",
        "expected_rows": 32951
    }
}

print("\n========== SPARK GOLD VALIDATION ==========")

successful = 0
failed = 0

# Validate each dataset
for dataset_name, details in GOLD_DATASETS.items():

    file_path = details["path"]
    expected_rows = details["expected_rows"]

    print(f"\nChecking: {dataset_name}")

    if not file_path.exists():
        print("FAILED: File not found")
        failed += 1
        continue

    try:
        parquet_file = pq.ParquetFile(file_path)

        actual_rows = parquet_file.metadata.num_rows
        columns = parquet_file.schema.names

        print("File exists: YES")
        print("Actual rows:", actual_rows)
        print("Expected rows:", expected_rows)
        print("Number of columns:", len(columns))

        if actual_rows == expected_rows:
            print("Validation: SUCCESS")
            successful += 1
        else:
            print("Validation: ROW COUNT MISMATCH")
            failed += 1

    except Exception as error:
        print("Validation failed:", error)
        failed += 1

# Final summary
print("\n========== VALIDATION SUMMARY ==========")
print("Successful datasets:", successful)
print("Failed datasets:", failed)

if failed == 0:
    print("\nAll Spark Gold datasets validated successfully!")
else:
    print("\nSome datasets need attention.")
