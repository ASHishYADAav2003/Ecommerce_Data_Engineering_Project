
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_DIR / "data" / "processed" / "silver"
GOLD_DIR = PROJECT_DIR / "data" / "gold" / "gold_reviews"

REVIEWS_FILE = SILVER_DIR / "reviews" / "reviews.parquet"
ORDERS_FILE = SILVER_DIR / "orders" / "orders.parquet"

OUTPUT_FILE = GOLD_DIR / "gold_reviews.parquet"

# 2. Create output directory
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load Silver datasets
reviews = pd.read_parquet(REVIEWS_FILE)
orders = pd.read_parquet(ORDERS_FILE)

print("Silver datasets loaded successfully.")
print("Reviews:", len(reviews))
print("Orders:", len(orders))

# 4. Join reviews with order information
gold_reviews = reviews.merge(
    orders[
        [
            "order_id",
            "customer_id",
            "order_purchase_timestamp",
            "order_status"
        ]
    ],
    on="order_id",
    how="left",
    validate="many_to_one"
)

# 5. Create review score categories
gold_reviews["review_category"] = "average"

gold_reviews.loc[
    gold_reviews["review_score"].isin([1, 2]),
    "review_category"
] = "negative"

gold_reviews.loc[
    gold_reviews["review_score"] == 3,
    "review_category"
] = "average"

gold_reviews.loc[
    gold_reviews["review_score"].isin([4, 5]),
    "review_category"
] = "positive"

# 6. Calculate review response time in days
gold_reviews["review_response_days"] = (
    gold_reviews["review_answer_timestamp"]
    - gold_reviews["review_creation_date"]
).dt.total_seconds() / 86400

# 7. Validate review scores
if not gold_reviews["review_score"].between(1, 5).all():
    raise ValueError("Invalid review scores found!")

# 8. Display review analysis
print("\nGOLD REVIEWS SUMMARY")
print("=" * 50)

print("Total review records:", len(gold_reviews))

print("\nReview score distribution:")
print(
    gold_reviews["review_score"]
    .value_counts()
    .sort_index()
)

print("\nReview category distribution:")
print(gold_reviews["review_category"].value_counts())

print(
    "\nAverage review score:",
    round(gold_reviews["review_score"].mean(), 2)
)

print(
    "\nAverage review response time (days):",
    round(gold_reviews["review_response_days"].mean(), 2)
)

# 9. Save Gold Reviews dataset
gold_reviews.to_parquet(OUTPUT_FILE, index=False)

print("\nGold Reviews dataset created successfully!")
print("Output file:", OUTPUT_FILE)
print("Final rows:", len(gold_reviews))
