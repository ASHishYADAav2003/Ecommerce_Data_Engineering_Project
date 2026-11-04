
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_DIR / "data" / "processed" / "silver"
GOLD_DIR = PROJECT_DIR / "data" / "gold" / "gold_orders"

ORDERS_FILE = SILVER_DIR / "orders" / "orders.parquet"
CUSTOMERS_FILE = SILVER_DIR / "customers" / "customers.parquet"

OUTPUT_FILE = GOLD_DIR / "gold_orders.parquet"

# 2. Create output directory
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load Silver datasets
orders = pd.read_parquet(ORDERS_FILE)
customers = pd.read_parquet(CUSTOMERS_FILE)

print("Silver datasets loaded successfully.")
print("Orders:", len(orders))
print("Customers:", len(customers))

# 4. Join orders with customer information
gold_orders = orders.merge(
    customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state"
        ]
    ],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# 5. Calculate delivery duration in days
gold_orders["delivery_days"] = (
    gold_orders["order_delivered_customer_date"]
    - gold_orders["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# 6. Calculate delivery delay in days
gold_orders["delivery_delay_days"] = (
    gold_orders["order_delivered_customer_date"]
    - gold_orders["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# 7. Create delivery performance category
gold_orders["delivery_status"] = "not_delivered"

gold_orders.loc[
    gold_orders["delivery_delay_days"] <= 0,
    "delivery_status"
] = "on_time_or_early"

gold_orders.loc[
    gold_orders["delivery_delay_days"] > 0,
    "delivery_status"
] = "delayed"

# 8. Validate order IDs
if gold_orders["order_id"].isnull().any():
    raise ValueError("Missing order IDs found!")

if gold_orders["order_id"].duplicated().any():
    raise ValueError("Duplicate order IDs found in Gold Orders!")

# 9. Display summary
print("\nGold Orders Summary")
print("=" * 50)

print("Total orders:", len(gold_orders))

print("\nOrder status distribution:")
print(gold_orders["order_status"].value_counts())

print("\nDelivery performance:")
print(gold_orders["delivery_status"].value_counts())

print("\nMissing values:")
print(gold_orders.isnull().sum())

# 10. Save Gold dataset
gold_orders.to_parquet(OUTPUT_FILE, index=False)

print("\nGold Orders dataset created successfully!")
print("Output file:", OUTPUT_FILE)
print("Final rows:", len(gold_orders))
