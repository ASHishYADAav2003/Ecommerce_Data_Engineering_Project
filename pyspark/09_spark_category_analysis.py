from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, round

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset paths
ITEMS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "order_items" / "order_items.parquet"
)

PRODUCTS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "products" / "products.parquet"
)

TRANSLATION_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "category_translation" / "category_translation.parquet"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkCategoryAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Load datasets
items_df = spark.read.parquet(str(ITEMS_FILE))
products_df = spark.read.parquet(str(PRODUCTS_FILE))
translation_df = spark.read.parquet(str(TRANSLATION_FILE))

# Join order items with products
items_products_df = items_df.join(
    products_df.select(
        "product_id",
        "product_category_name"
    ),
    on="product_id",
    how="left"
)

# Join with category translation
category_sales_df = items_products_df.join(
    translation_df,
    on="product_category_name",
    how="left"
)

# Calculate revenue by category
category_analysis_df = category_sales_df.groupBy(
    "product_category_name_english"
).agg(
    count("*").alias("total_items_sold"),
    round(sum("price"), 2).alias("total_revenue")
)

# Display top 10 categories
print("\nTop 10 Categories by Revenue:")

category_analysis_df.orderBy(
    col("total_revenue").desc()
).show(10, truncate=False)

# Display total category records
print(
    "\nTotal Category Groups:",
    category_analysis_df.count()
)

# Stop Spark
spark.stop()