
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_DIR / "data" / "processed" / "silver"
GOLD_DIR = PROJECT_DIR / "data" / "gold" / "gold_sellers"

SELLERS_FILE = SILVER_DIR / "sellers" / "sellers.parquet"
ITEMS_FILE = SILVER_DIR / "order_items" / "order_items.parquet"
ORDERS_FILE = SILVER_DIR / "orders" / "orders.parquet"

OUTPUT_FILE = GOLD_DIR / "gold_sellers.parquet"

# 2. Create output directory
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load Silver datasets
sellers = pd.read_parquet(SELLERS_FILE)
items = pd.read_parquet(ITEMS_FILE)
orders = pd.read_parquet(ORDERS_FILE)

print("Silver datasets loaded successfully.")

# 4. Join order items with orders to get customer IDs
seller_sales = items.merge(
    orders[["order_id", "customer_id"]],
    on="order_id",
    how="left",
    validate="many_to_one"
)

# 5. Calculate seller-level metrics
seller_metrics = (
    seller_sales.groupby("seller_id", as_index=False)
    .agg(
        total_items_sold=("order_item_id", "count"),
        total_orders=("order_id", "nunique"),
        total_product_revenue=("price", "sum"),
        total_freight=("freight_value", "sum"),
        average_product_price=("price", "mean"),
        unique_customers=("customer_id", "nunique")
    )
)

# 6. Join seller information with performance metrics
gold_sellers = sellers.merge(
    seller_metrics,
    on="seller_id",
    how="left",
    validate="one_to_one"
)

# 7. Fill missing sales metrics with zero
metric_columns = [
    "total_items_sold",
    "total_orders",
    "total_product_revenue",
    "total_freight",
    "unique_customers"
]

gold_sellers[metric_columns] = (
    gold_sellers[metric_columns].fillna(0)
)

# 8. Validate seller IDs
if gold_sellers["seller_id"].isnull().any():
    raise ValueError("Missing seller IDs found!")

if gold_sellers["seller_id"].duplicated().any():
    raise ValueError("Duplicate seller IDs found!")

# 9. Display summary
print("\nGOLD SELLERS SUMMARY")
print("=" * 50)

print("Total sellers:", len(gold_sellers))
print("Sellers with sales:", (gold_sellers["total_orders"] > 0).sum())
print("Total items sold:", gold_sellers["total_items_sold"].sum())
print("Total product revenue:", gold_sellers["total_product_revenue"].sum())

# 10. Display top 10 sellers
print("\nTOP 10 SELLERS BY PRODUCT REVENUE")

top_sellers = gold_sellers.sort_values(
    "total_product_revenue",
    ascending=False
)

print(
    top_sellers[
        [
            "seller_id",
            "seller_city",
            "seller_state",
            "total_orders",
            "total_items_sold",
            "total_product_revenue"
        ]
    ].head(10).to_string(index=False)
)

# 11. Save Gold Sellers dataset
gold_sellers.to_parquet(OUTPUT_FILE, index=False)

print("\nGold Sellers dataset created successfully!")
print("Output file:", OUTPUT_FILE)
print("Final rows:", len(gold_sellers))
