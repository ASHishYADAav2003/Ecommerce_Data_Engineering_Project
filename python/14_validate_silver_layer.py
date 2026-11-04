
from pathlib import Path
import pyarrow.parquet as pq

# 1. Define project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_DIR / "data" / "processed" / "silver"

# 2. List all nine expected Parquet files
datasets = {
    "Customers": "customers/customers.parquet",
    "Orders": "orders/orders.parquet",
    "Order Items": "order_items/order_items.parquet",
    "Payments": "payments/payments.parquet",
    "Reviews": "reviews/reviews.parquet",
    "Products": "products/products.parquet",
    "Sellers": "sellers/sellers.parquet",
    "Geolocation": "geolocation/geolocation.parquet",
    "Category Translation": (
        "category_translation/category_translation.parquet"
    )
}

# 3. Initialize validation counters
successful = 0
failed = 0

print("=" * 70)
print("SILVER LAYER VALIDATION REPORT")
print("=" * 70)

# 4. Check every dataset
for dataset_name, relative_path in datasets.items():

    file_path = SILVER_DIR / relative_path

    print(f"\nDataset: {dataset_name}")

    # Check whether the file exists
    if not file_path.exists():
        print("Status: FAILED - File not found")
        failed += 1
        continue

    try:
        # Read Parquet metadata
        parquet_file = pq.ParquetFile(file_path)

        row_count = parquet_file.metadata.num_rows
        column_names = parquet_file.schema_arrow.names
        file_size_kb = file_path.stat().st_size / 1024

        print("Status: SUCCESS")
        print("Rows:", row_count)
        print("Columns:", len(column_names))
        print("Column names:", column_names)
        print(f"File size: {file_size_kb:.2f} KB")

        successful += 1

    except Exception as error:
        print("Status: FAILED")
        print("Error:", error)
        failed += 1

# 5. Print final summary
print("\n" + "=" * 70)
print("FINAL VALIDATION SUMMARY")
print("=" * 70)

print("Total datasets:", len(datasets))
print("Successful datasets:", successful)
print("Failed datasets:", failed)

if failed == 0:
    print("\nALL SILVER DATASETS PASSED VALIDATION!")
else:
    print("\nSOME DATASETS NEED ATTENTION.")
