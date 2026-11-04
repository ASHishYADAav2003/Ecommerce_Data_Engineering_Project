
from pathlib import Path
import shutil

import pyarrow as pa
import pyarrow.parquet as pq

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct, count, sum, round

# 1. Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 2. Input paths
CUSTOMERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "customers" / "customers.parquet"
)

ORDERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "orders" / "orders.parquet"
)

ITEMS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "order_items" / "order_items.parquet"
)

# 3. Output path
OUTPUT_DIR = (
    PROJECT_DIR / "data" / "gold"
    / "spark_gold_customers"
)

# 4. Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkGoldCustomers")
    .master("local[*]")
    .getOrCreate()
)

# 5. Load Silver datasets
customers_df = spark.read.parquet(str(CUSTOMERS_FILE))
orders_df = spark.read.parquet(str(ORDERS_FILE))
items_df = spark.read.parquet(str(ITEMS_FILE))

# 6. Calculate revenue for each order
order_spending_df = items_df.groupBy(
    "order_id"
).agg(
    round(
        sum(col("price") + col("freight_value")), 2
    ).alias("order_spending"),
    count("*").alias("total_items")
)

# 7. Join orders with order spending
customer_orders_df = orders_df.join(
    order_spending_df,
    on="order_id",
    how="left"
)

# 8. Aggregate customer-level metrics
customer_metrics_df = customer_orders_df.groupBy(
    "customer_id"
).agg(
    countDistinct("order_id").alias("total_orders"),
    round(
        sum("order_spending"), 2
    ).alias("total_spent"),
    sum("total_items").alias("total_items_purchased")
)

# 9. Join customer information with metrics
gold_customers_df = customers_df.join(
    customer_metrics_df,
    on="customer_id",
    how="left"
)

# 10. Replace missing metrics with zero
gold_customers_df = gold_customers_df.fillna({
    "total_orders": 0,
    "total_spent": 0,
    "total_items_purchased": 0
})

# 11. Display record count
print("\nGold Customers Record Count:", gold_customers_df.count())

print("\nGold Customers Sample:")
gold_customers_df.show(5, truncate=False)

# 12. Convert Spark DataFrame to Pandas
gold_customers_pandas = gold_customers_df.toPandas()

# 13. Convert Pandas to Arrow Table
gold_customers_table = pa.Table.from_pandas(
    gold_customers_pandas,
    preserve_index=False
)

# 14. Prepare output folder
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 15. Save Parquet using PyArrow
OUTPUT_FILE = OUTPUT_DIR / "gold_customers.parquet"

pq.write_table(
    gold_customers_table,
    OUTPUT_FILE,
    compression="snappy"
)

print("\nGold Customers dataset saved successfully!")
print("Output location:", OUTPUT_FILE)

# 16. Stop Spark
spark.stop()
