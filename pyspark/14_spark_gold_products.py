
from pathlib import Path
import shutil

import pyarrow as pa
import pyarrow.parquet as pq

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg, round

# 1. Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 2. Input paths
PRODUCTS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "products" / "products.parquet"
)

ITEMS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "order_items" / "order_items.parquet"
)

TRANSLATION_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "category_translation" / "category_translation.parquet"
)

# 3. Output path
OUTPUT_DIR = (
    PROJECT_DIR / "data" / "gold"
    / "spark_gold_products"
)

# 4. Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkGoldProducts")
    .master("local[*]")
    .getOrCreate()
)

# 5. Load Silver datasets
products_df = spark.read.parquet(str(PRODUCTS_FILE))
items_df = spark.read.parquet(str(ITEMS_FILE))
translation_df = spark.read.parquet(str(TRANSLATION_FILE))

# 6. Calculate product-level sales metrics
product_metrics_df = items_df.groupBy(
    "product_id"
).agg(
    count("*").alias("units_sold"),
    round(sum("price"), 2).alias("total_revenue"),
    round(avg("price"), 2).alias("average_price"),
    round(sum("freight_value"), 2).alias("total_freight")
)

# 7. Join products with sales metrics
gold_products_df = products_df.join(
    product_metrics_df,
    on="product_id",
    how="left"
)

# 8. Replace missing sales metrics with zero
gold_products_df = gold_products_df.fillna({
    "units_sold": 0,
    "total_revenue": 0,
    "total_freight": 0
})

# 9. Join category translation
gold_products_df = gold_products_df.join(
    translation_df,
    on="product_category_name",
    how="left"
)

# 10. Display record count
print("\nGold Products Record Count:", gold_products_df.count())

print("\nGold Products Sample:")
gold_products_df.show(5, truncate=False)

# 11. Convert Spark DataFrame to Pandas
gold_products_pandas = gold_products_df.toPandas()

# 12. Convert to Arrow Table
gold_products_table = pa.Table.from_pandas(
    gold_products_pandas,
    preserve_index=False
)

# 13. Prepare output folder
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 14. Save Parquet using PyArrow
OUTPUT_FILE = OUTPUT_DIR / "gold_products.parquet"

pq.write_table(
    gold_products_table,
    OUTPUT_FILE,
    compression="snappy"
)

print("\nGold Products dataset saved successfully!")
print("Output location:", OUTPUT_FILE)

# 15. Stop Spark
spark.stop()
