
from pathlib import Path
import shutil

import pyarrow as pa
import pyarrow.parquet as pq

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, date_format

# 1. Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 2. Input paths
ITEMS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "order_items" / "order_items.parquet"
)

ORDERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "orders" / "orders.parquet"
)

PRODUCTS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "products" / "products.parquet"
)

TRANSLATION_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "category_translation" / "category_translation.parquet"
)

# 3. Output path
OUTPUT_DIR = (
    PROJECT_DIR / "data" / "gold"
    / "spark_gold_revenue"
)

# 4. Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkGoldRevenue")
    .master("local[*]")
    .getOrCreate()
)

# 5. Load Silver datasets
items_df = spark.read.parquet(str(ITEMS_FILE))
orders_df = spark.read.parquet(str(ORDERS_FILE))
products_df = spark.read.parquet(str(PRODUCTS_FILE))
translation_df = spark.read.parquet(str(TRANSLATION_FILE))

# 6. Select required order columns
orders_selected_df = orders_df.select(
    "order_id",
    "order_status",
    "order_purchase_timestamp"
)

# 7. Select required product columns
products_selected_df = products_df.select(
    "product_id",
    "product_category_name"
)

# 8. Join order items with orders
gold_revenue_df = items_df.join(
    orders_selected_df,
    on="order_id",
    how="left"
)

# 9. Join with products
gold_revenue_df = gold_revenue_df.join(
    products_selected_df,
    on="product_id",
    how="left"
)

# 10. Join with category translation
gold_revenue_df = gold_revenue_df.join(
    translation_df,
    on="product_category_name",
    how="left"
)

# 11. Calculate item value including freight
gold_revenue_df = gold_revenue_df.withColumn(
    "total_item_value",
    round(
        col("price") + col("freight_value"),
        2
    )
)

# 12. Extract purchase month
gold_revenue_df = gold_revenue_df.withColumn(
    "purchase_month",
    date_format(
        col("order_purchase_timestamp"),
        "yyyy-MM"
    )
)

# 13. Display record count
print("\nGold Revenue Record Count:", gold_revenue_df.count())

print("\nGold Revenue Sample:")
gold_revenue_df.show(5, truncate=False)

# 14. Convert Spark DataFrame to Pandas
gold_revenue_pandas = gold_revenue_df.toPandas()

# 15. Convert to Arrow Table
gold_revenue_table = pa.Table.from_pandas(
    gold_revenue_pandas,
    preserve_index=False
)

# 16. Prepare output folder
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 17. Save Parquet using PyArrow
OUTPUT_FILE = OUTPUT_DIR / "gold_revenue.parquet"

pq.write_table(
    gold_revenue_table,
    OUTPUT_FILE,
    compression="snappy"
)

print("\nGold Revenue dataset saved successfully!")
print("Output location:", OUTPUT_FILE)

# 18. Stop Spark
spark.stop()
