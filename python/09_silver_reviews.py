
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "olist_order_reviews_dataset.csv"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "silver" / "reviews"
OUTPUT_FILE = OUTPUT_DIR / "reviews.parquet"

# 2. Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load raw reviews dataset
reviews = pd.read_csv(RAW_FILE)

print("Raw reviews dataset loaded.")
print("Rows before cleaning:", len(reviews))

# 4. Clean text columns
text_columns = [
    "review_id",
    "order_id",
    "review_comment_title",
    "review_comment_message"
]

for column in text_columns:
    reviews[column] = reviews[column].str.strip()

# 5. Convert review creation and answer timestamps
date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in date_columns:
    reviews[column] = pd.to_datetime(
        reviews[column],
        errors="coerce"
    )

# 6. Validate required identifiers
required_columns = ["review_id", "order_id"]

for column in required_columns:
    if reviews[column].isnull().any():
        raise ValueError(f"Missing values found in {column}!")

# 7. Validate composite key
if reviews.duplicated(
    subset=["review_id", "order_id"]
).any():
    raise ValueError("Duplicate (review_id, order_id) pairs found!")

# 8. Validate review scores
if not reviews["review_score"].between(1, 5).all():
    raise ValueError("Invalid review scores found!")

# 9. Display review score distribution
print("\nReview score distribution:")
print(reviews["review_score"].value_counts().sort_index())

# 10. Display missing values
print("\nMissing values after cleaning:")
print(reviews.isnull().sum())

# 11. Save all review records as Parquet
reviews.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Reviews dataset created successfully!")
print("Rows after cleaning:", len(reviews))
print("Output file:", OUTPUT_FILE)
