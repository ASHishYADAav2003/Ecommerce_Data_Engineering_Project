from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Orders Parquet path
ORDERS_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "silver"
    / "orders"
    / "orders.parquet"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkOrderAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Load orders
orders_df = spark.read.parquet(str(ORDERS_FILE))

# 1. Select important columns
selected_df = orders_df.select(
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp"
)

print("\nSelected Order Columns:")
selected_df.show(5, truncate=False)

# 2. Filter delivered orders
delivered_df = orders_df.filter(
    col("order_status") == "delivered"
)

print("\nTotal Delivered Orders:", delivered_df.count())

# 3. Group orders by status
status_df = orders_df.groupBy(
    "order_status"
).agg(
    count("order_id").alias("total_orders")
)

print("\nOrders by Status:")
status_df.orderBy(
    col("total_orders").desc()
).show(truncate=False)

# Stop Spark
spark.stop()