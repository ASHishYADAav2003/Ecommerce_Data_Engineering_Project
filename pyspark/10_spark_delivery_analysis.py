
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    datediff,
    avg,
    count,
    round,
    sum
)

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
ORDERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "orders" / "orders.parquet"
)

CUSTOMERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "customers" / "customers.parquet"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkDeliveryAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Load datasets
orders_df = spark.read.parquet(str(ORDERS_FILE))
customers_df = spark.read.parquet(str(CUSTOMERS_FILE))

# Select customer location columns
customers_selected_df = customers_df.select(
    "customer_id",
    "customer_state"
)

# Join orders with customers
orders_df = orders_df.join(
    customers_selected_df,
    on="customer_id",
    how="left"
)

# Calculate actual delivery days
delivery_df = orders_df.withColumn(
    "actual_delivery_days",
    datediff(
        col("order_delivered_customer_date"),
        col("order_purchase_timestamp")
    )
)

# Calculate estimated delivery days
delivery_df = delivery_df.withColumn(
    "estimated_delivery_days",
    datediff(
        col("order_estimated_delivery_date"),
        col("order_purchase_timestamp")
    )
)

# Calculate delivery delay
delivery_df = delivery_df.withColumn(
    "delivery_delay_days",
    datediff(
        col("order_delivered_customer_date"),
        col("order_estimated_delivery_date")
    )
)

# Average delivery metrics
print("\nAverage Delivery Metrics:")

delivery_df.select(
    round(avg("actual_delivery_days"), 2).alias(
        "avg_actual_delivery_days"
    ),
    round(avg("estimated_delivery_days"), 2).alias(
        "avg_estimated_delivery_days"
    ),
    round(avg("delivery_delay_days"), 2).alias(
        "avg_delivery_delay_days"
    )
).show()

# Count late deliveries
print("\nLate Delivery Count:")

delivery_df.filter(
    col("delivery_delay_days") > 0
).agg(
    count("*").alias("late_deliveries")
).show()

# Delivery performance by customer state
print("\nDelivery Performance by State:")

delivery_df.groupBy(
    "customer_state"
).agg(
    count("*").alias("total_orders"),
    round(avg("actual_delivery_days"), 2).alias(
        "avg_delivery_days"
    ),
    sum(
        (col("delivery_delay_days") > 0).cast("int")
    ).alias("late_deliveries")
).orderBy(
    col("total_orders").desc()
).show(30, truncate=False)

# Stop Spark
spark.stop()
