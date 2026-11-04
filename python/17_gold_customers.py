
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_DIR / "data" / "processed" / "silver"
GOLD_DIR = PROJECT_DIR / "data" / "gold" / "gold_customers"

CUSTOMERS_FILE = SILVER_DIR / "customers" / "customers.parquet"
ORDERS_FILE = SILVER_DIR / "orders" / "orders.parquet"
ITEMS_FILE = SILVER_DIR / "order_items" / "order_items.parquet"

OUTPUT_FILE = GOLD_DIR / "gold_customers.parquet"

# 2. Create output directory
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load Silver datasets
customers = pd.read_parquet(CUSTOMERS_FILE)
orders = pd.read_parquet(ORDERS_FILE)
items = pd.read_parquet(ITEMS_FILE)

print("Silver datasets loaded successfully.")

# 4. Calculate total order value for each order
order_values = (
    items.groupby("order_id", as_index=False)
    .agg(
        order_revenue=("price", "sum"),
        order_freight=("freight_value", "sum")
    )
)

order_values["total_order_value"] = (
    order_values["order_revenue"]
    + order_values["order_freight"]
)

# 5. Join orders with order values
customer_orders = orders.merge(
    order_values,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# 6. Calculate customer-level metrics
customer_metrics = (
    customer_orders.groupby("customer_id", as_index=False)
    .agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("order_revenue", "sum"),
        total_freight=("order_freight", "sum"),
        total_spent=("total_order_value", "sum"),
        first_order_date=("order_purchase_timestamp", "min"),
        last_order_date=("order_purchase_timestamp", "max")
    )
)

customer_metrics["average_order_value"] = (
    customer_metrics["total_spent"]
    / customer_metrics["total_orders"]
)

# 7. Join customer information
gold_customers = customers.merge(
    customer_metrics,
    on="customer_id",
    how="left",
    validate="one_to_one"
)

# 8. Validate customer records
if gold_customers["customer_id"].duplicated().any():
    raise ValueError("Duplicate customer records found!")

if gold_customers["customer_id"].isnull().any():
    raise ValueError("Missing customer IDs found!")

# 9. Display summary
print("\nGOLD CUSTOMERS SUMMARY")
print("=" * 50)

print("Total customers:", len(gold_customers))
print("Total orders:", gold_customers["total_orders"].sum())
print("Total customer spending:", gold_customers["total_spent"].sum())

print("\nTop 10 customers by spending:")

top_customers = gold_customers.sort_values(
    "total_spent",
    ascending=False
)

print(
    top_customers[
        [
            "customer_unique_id",
            "customer_city",
            "customer_state",
            "total_orders",
            "total_spent"
        ]
    ].head(10).to_string(index=False)
)

# 10. Save Gold Customers dataset
gold_customers.to_parquet(OUTPUT_FILE, index=False)

print("\nGold Customers dataset created successfully!")
print("Output file:", OUTPUT_FILE)
print("Final rows:", len(gold_customers))
