from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
CUSTOMERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "customers" / "customers.parquet"
)

ORDERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "orders" / "orders.parquet"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkCustomerAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Load datasets
customers_df = spark.read.parquet(str(CUSTOMERS_FILE))
orders_df = spark.read.parquet(str(ORDERS_FILE))

# Count orders per customer
customer_orders_df = orders_df.groupBy(
    "customer_id"
).agg(
    countDistinct("order_id").alias("total_orders")
)

# Join customer information with order counts
customer_analysis_df = customers_df.join(
    customer_orders_df,
    on="customer_id",
    how="left"
)

# Replace missing order counts with zero
customer_analysis_df = customer_analysis_df.fillna(
    {"total_orders": 0}
)

# Display total customers
print(
    "\nTotal Customer Records:",
    customer_analysis_df.count()
)

# Display customers with most orders
print("\nTop 10 Customers by Number of Orders:")

customer_analysis_df.select(
    "customer_unique_id",
    "customer_city",
    "customer_state",
    "total_orders"
).orderBy(
    col("total_orders").desc()
).show(10, truncate=False)

# Count distinct real customer identities
print(
    "\nUnique Customer Identities:",
    customer_analysis_df.select(
        "customer_unique_id"
    ).distinct().count()
)

# Stop Spark
spark.stop()