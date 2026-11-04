from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, round

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Order items Parquet path
ITEMS_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "silver"
    / "order_items"
    / "order_items.parquet"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkProductAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Load order items
items_df = spark.read.parquet(str(ITEMS_FILE))

# Calculate item revenue
items_df = items_df.withColumn(
    "item_revenue",
    col("price") + col("freight_value")
)

# Group by product
product_sales_df = items_df.groupBy(
    "product_id"
).agg(
    sum("order_item_id").alias("units_sold"),
    round(sum("price"), 2).alias("total_product_revenue"),
    round(sum("freight_value"), 2).alias("total_freight")
)

# Display top 10 products by revenue
print("\nTop 10 Products by Revenue:")

product_sales_df.orderBy(
    col("total_product_revenue").desc()
).show(10, truncate=False)

# Display total number of products sold
print(
    "\nTotal Product Records:",
    product_sales_df.count()
)

# Stop Spark
spark.stop()