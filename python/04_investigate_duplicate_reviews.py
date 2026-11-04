
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")

# Find all records with duplicate review IDs
duplicates = reviews[
    reviews.duplicated(subset=["review_id"], keep=False)
].copy()

# Sort records to make comparison easier
duplicates = duplicates.sort_values("review_id")

# Count duplicate IDs
duplicate_id_count = duplicates["review_id"].nunique()

# Check for completely identical rows
identical_row_count = duplicates.duplicated().sum()

# Check whether duplicate IDs have different order IDs
order_variations = (
    duplicates.groupby("review_id")["order_id"].nunique()
)

different_order_count = (order_variations > 1).sum()

print("=" * 60)
print("DUPLICATE REVIEW INVESTIGATION")
print("=" * 60)

print(f"Total review records: {len(reviews)}")
print(f"Records with duplicate review IDs: {len(duplicates)}")
print(f"Unique duplicate review IDs: {duplicate_id_count}")
print(f"Completely identical duplicate rows: {identical_row_count}")
print(f"Duplicate IDs linked to multiple orders: {different_order_count}")

print("\nFirst 20 duplicate records:")
print(duplicates.head(20).to_string(index=False))

# Save the investigation results
output_file = REPORT_DIR / "duplicate_reviews_inspection.csv"
duplicates.to_csv(output_file, index=False)

print(f"\nInvestigation file saved at: {output_file}")

# Validate the composite review key
composite_duplicates = reviews.duplicated(
    subset=["review_id", "order_id"]
).sum()

print("\nCOMPOSITE KEY VALIDATION")
print("=" * 40)
print("Duplicate (review_id, order_id) pairs:", composite_duplicates)
