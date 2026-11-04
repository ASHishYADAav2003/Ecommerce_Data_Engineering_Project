
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_DIR / "data" / "processed" / "silver"
GOLD_DIR = PROJECT_DIR / "data" / "gold" / "gold_revenue"

ITEMS_FILE = SILVER_DIR / "order_items" / "order_items.parquet"
ORDERS_FILE = SILVER_DIR / "orders" / "orders.parquet"
PRODUCTS_FILE = SILVER_DIR / "products" / "products.parquet"
CATEGORIES_FILE = (
    SILVER_DIR / "category_translation" / "category_translation.parquet"
)

OUTPUT_FILE = GOLD_DIR / "gold_revenue.parquet"

# 2. Create output directory
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load Silver datasets
items = pd.read_parquet(ITEMS_FILE)
orders = pd.read_parquet(ORDERS_FILE)
products = pd.read_parquet(PRODUCTS_FILE)
categories = pd.read_parquet(CATEGORIES_FILE)

print("Silver datasets loaded successfully.")

# 4. Join order items with orders
revenue = items.merge(
    orders[["order_id", "order_purchase_timestamp", "order_status"]],
    on="order_id",
    how="left",
    validate="many_to_one"
)

# 5. Join product information
revenue = revenue.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left",
    validate="many_to_one"
)

# 6. Join English category translations
revenue = revenue.merge(
    categories,
    on="product_category_name",
    how="left",
    validate="many_to_one"
)

# 7. Create revenue measures
revenue["total_item_revenue"] = revenue["price"]
revenue["total_freight_revenue"] = revenue["freight_value"]

revenue["total_order_item_value"] = (
    revenue["total_item_revenue"]
    + revenue["total_freight_revenue"]
)

# 8. Extract purchase month
revenue["purchase_month"] = (
    revenue["order_purchase_timestamp"].dt.to_period("M").astype("string")
)

# 9. Display revenue summary
print("\nGOLD REVENUE SUMMARY")
print("=" * 50)

print("Total order item records:", len(revenue))
print("Total product revenue:", revenue["total_item_revenue"].sum())
print("Total freight value:", revenue["total_freight_revenue"].sum())
print("Total item plus freight value:", revenue["total_order_item_value"].sum())
print("Unique orders:", revenue["order_id"].nunique())

# 10. Calculate monthly revenue
monthly_revenue = (
    revenue.groupby("purchase_month", as_index=False)
    .agg(
        total_revenue=("total_item_revenue", "sum"),
        total_freight=("total_freight_revenue", "sum"),
        order_count=("order_id", "nunique")
    )
)

print("\nMONTHLY REVENUE (FIRST 10 MONTHS)")
print(monthly_revenue.head(10).to_string(index=False))

# 11. Save detailed Gold Revenue dataset
revenue.to_parquet(OUTPUT_FILE, index=False)

print("\nGold Revenue dataset created successfully!")
print("Output file:", OUTPUT_FILE)
print("Final rows:", len(revenue))
