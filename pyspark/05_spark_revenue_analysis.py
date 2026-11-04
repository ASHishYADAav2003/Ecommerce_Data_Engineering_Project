from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum,
    date_format,
    round
)

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
ORDERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "orders" / "orders.parquet"
)

ITEMS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "order_items" / "order_items.parquet"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkRevenueAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Load datasets
orders_df = spark.read.parquet(str(ORDERS_FILE))
items_df = spark.read.parquet(str(ITEMS_FILE))

# Join order items with orders
revenue_df = items_df.join(
    orders_df.select(
        "order_id",
        "order_purchase_timestamp",
        "order_status"
    ),
    on="order_id",
    how="inner"
)

# Calculate item value including freight
revenue_df = revenue_df.withColumn(
    "total_item_value",
    col("price") + col("freight_value")
)

# Extract purchase month
revenue_df = revenue_df.withColumn(
    "purchase_month",
    date_format(
        col("order_purchase_timestamp"),
        "yyyy-MM"
    )
)

# Calculate monthly revenue
monthly_revenue_df = revenue_df.groupBy(
    "purchase_month"
).agg(
    round(
        sum("total_item_value"), 2
    ).alias("monthly_revenue")
)

# Display monthly revenue
print("\nMonthly Revenue:")

monthly_revenue_df.orderBy(
    "purchase_month"
).show(50, truncate=False)

# Calculate overall item value
print("\nTotal Order Item Value:")

revenue_df.select(
    round(
        sum("total_item_value"), 2
    ).alias("total_order_item_value")
).show()

# Stop Spark
spark.stop()