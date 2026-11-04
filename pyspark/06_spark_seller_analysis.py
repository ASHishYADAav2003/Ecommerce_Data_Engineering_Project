from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, countDistinct, sum, round
)

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
SELLERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "sellers" / "sellers.parquet"
)

ITEMS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "order_items" / "order_items.parquet"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkSellerAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Load datasets
sellers_df = spark.read.parquet(str(SELLERS_FILE))
items_df = spark.read.parquet(str(ITEMS_FILE))

# Calculate seller-level sales metrics
seller_sales_df = items_df.groupBy(
    "seller_id"
).agg(
    count("*").alias("total_items_sold"),
    countDistinct("order_id").alias("total_orders"),
    round(sum("price"), 2).alias("total_revenue"),
    round(sum("freight_value"), 2).alias("total_freight")
)

# Join seller details with sales metrics
seller_analysis_df = sellers_df.join(
    seller_sales_df,
    on="seller_id",
    how="left"
)

# Replace missing sales metrics with zero
seller_analysis_df = seller_analysis_df.fillna({
    "total_items_sold": 0,
    "total_orders": 0,
    "total_revenue": 0,
    "total_freight": 0
})

# Display total sellers
print("\nTotal Sellers:", seller_analysis_df.count())

# Display top 10 sellers by revenue
print("\nTop 10 Sellers by Revenue:")

seller_analysis_df.select(
    "seller_id",
    "seller_state",
    "total_items_sold",
    "total_orders",
    "total_revenue"
).orderBy(
    col("total_revenue").desc()
).show(10, truncate=False)

# Display seller revenue by state
print("\nSeller Revenue by State:")

seller_analysis_df.groupBy(
    "seller_state"
).agg(
    round(sum("total_revenue"), 2).alias("state_revenue")
).orderBy(
    col("state_revenue").desc()
).show(truncate=False)

# Stop Spark
spark.stop()