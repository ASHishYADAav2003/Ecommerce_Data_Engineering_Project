
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_DIR / "data" / "processed" / "silver"
GOLD_DIR = PROJECT_DIR / "data" / "gold" / "gold_products"

PRODUCTS_FILE = SILVER_DIR / "products" / "products.parquet"
ITEMS_FILE = SILVER_DIR / "order_items" / "order_items.parquet"
CATEGORIES_FILE = (
    SILVER_DIR / "category_translation" / "category_translation.parquet"
)

OUTPUT_FILE = GOLD_DIR / "gold_products.parquet"

# 2. Create output directory
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load Silver datasets
products = pd.read_parquet(PRODUCTS_FILE)
items = pd.read_parquet(ITEMS_FILE)
categories = pd.read_parquet(CATEGORIES_FILE)

print("Silver datasets loaded successfully.")

# 4. Calculate product-level sales metrics
product_metrics = (
    items.groupby("product_id", as_index=False)
    .agg(
        units_sold=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        total_freight=("freight_value", "sum"),
        average_price=("price", "mean"),
        unique_orders=("order_id", "nunique")
    )
)

# 5. Join product details with sales metrics
gold_products = products.merge(
    product_metrics,
    on="product_id",
    how="left",
    validate="one_to_one"
)

# 6. Join English category translations
gold_products = gold_products.merge(
    categories,
    on="product_category_name",
    how="left",
    validate="many_to_one"
)

# 7. Fill missing sales metrics for products without sales
sales_columns = [
    "units_sold",
    "total_revenue",
    "total_freight",
    "unique_orders"
]

gold_products[sales_columns] = (
    gold_products[sales_columns].fillna(0)
)

# 8. Validate product IDs
if gold_products["product_id"].isnull().any():
    raise ValueError("Missing product IDs found!")

if gold_products["product_id"].duplicated().any():
    raise ValueError("Duplicate product IDs found!")

# 9. Display summary
print("\nGOLD PRODUCTS SUMMARY")
print("=" * 50)

print("Total products:", len(gold_products))
print("Products with sales:", (gold_products["units_sold"] > 0).sum())
print("Total units sold:", gold_products["units_sold"].sum())
print("Total product revenue:", gold_products["total_revenue"].sum())

# 10. Top 10 products by revenue
print("\nTOP 10 PRODUCTS BY REVENUE")

top_products = gold_products.sort_values(
    "total_revenue",
    ascending=False
)

print(
    top_products[
        [
            "product_id",
            "product_category_name_english",
            "units_sold",
            "total_revenue"
        ]
    ].head(10).to_string(index=False)
)

# 11. Save Gold Products dataset
gold_products.to_parquet(OUTPUT_FILE, index=False)

print("\nGold Products dataset created successfully!")
print("Output file:", OUTPUT_FILE)
print("Final rows:", len(gold_products))
