
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")
products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
sellers = pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv")

results = []

def add_result(check, value):
    results.append({
        "Check": check,
        "Result": value
    })

# 1. Row counts
for name, df in [
    ("Customers", customers),
    ("Orders", orders),
    ("Order Items", items),
    ("Payments", payments),
    ("Reviews", reviews),
    ("Products", products),
    ("Sellers", sellers)
]:
    add_result(f"{name} row count", len(df))

# 2. Missing important IDs
key_columns = [
    (customers, "customer_id", "Customers"),
    (orders, "order_id", "Orders"),
    (orders, "customer_id", "Orders"),
    (items, "order_id", "Order Items"),
    (items, "product_id", "Order Items"),
    (items, "seller_id", "Order Items"),
    (payments, "order_id", "Payments"),
    (reviews, "order_id", "Reviews"),
    (products, "product_id", "Products"),
    (sellers, "seller_id", "Sellers")
]

for df, column, name in key_columns:
    missing = df[column].isnull().sum()
    add_result(f"{name} missing {column}", missing)

# 3. Duplicate key checks
duplicate_checks = [
    (customers, ["customer_id"], "Customers"),
    (orders, ["order_id"], "Orders"),
    (items, ["order_id", "order_item_id"], "Order Items"),
    (payments, ["order_id", "payment_sequential"], "Payments"),
    (reviews, ["review_id"], "Reviews"),
    (products, ["product_id"], "Products"),
    (sellers, ["seller_id"], "Sellers")
]

for df, columns, name in duplicate_checks:
    duplicates = df.duplicated(subset=columns).sum()
    add_result(f"{name} duplicate keys", duplicates)

# 4. Referential integrity checks
add_result(
    "Orders without matching customers",
    (~orders["customer_id"].isin(customers["customer_id"])).sum()
)

add_result(
    "Order items without matching orders",
    (~items["order_id"].isin(orders["order_id"])).sum()
)

add_result(
    "Order items without matching products",
    (~items["product_id"].isin(products["product_id"])).sum()
)

add_result(
    "Order items without matching sellers",
    (~items["seller_id"].isin(sellers["seller_id"])).sum()
)

add_result(
    "Payments without matching orders",
    (~payments["order_id"].isin(orders["order_id"])).sum()
)

add_result(
    "Reviews without matching orders",
    (~reviews["order_id"].isin(orders["order_id"])).sum()
)

# 5. Display and save report
report = pd.DataFrame(results)

print("\nECOMMERCE DATA QUALITY REPORT")
print("=" * 60)
print(report.to_string(index=False))

output_file = REPORT_DIR / "data_quality_report.csv"
report.to_csv(output_file, index=False)

print("\nReport saved successfully!")
print(output_file)
