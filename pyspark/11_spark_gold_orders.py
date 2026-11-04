
from pathlib import Path
import shutil

import pyarrow as pa
import pyarrow.parquet as pq

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, datediff, when

# --------------------------------------------------
# 1. Find project folder
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# 2. Input dataset paths
# --------------------------------------------------

ORDERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "orders" / "orders.parquet"
)

CUSTOMERS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "customers" / "customers.parquet"
)

# --------------------------------------------------
# 3. Output path
# --------------------------------------------------

OUTPUT_DIR = (
    PROJECT_DIR / "data" / "gold"
    / "spark_gold_orders"
)

# --------------------------------------------------
# 4. Create Spark session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("SparkGoldOrders")
    .master("local[*]")
    .getOrCreate()
)

# --------------------------------------------------
# 5. Load Silver datasets
# --------------------------------------------------

orders_df = spark.read.parquet(str(ORDERS_FILE))
customers_df = spark.read.parquet(str(CUSTOMERS_FILE))

# --------------------------------------------------
# 6. Select customer information
# --------------------------------------------------

customers_selected_df = customers_df.select(
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state"
)

# --------------------------------------------------
# 7. Join orders with customers
# --------------------------------------------------

gold_orders_df = orders_df.join(
    customers_selected_df,
    on="customer_id",
    how="left"
)

# --------------------------------------------------
# 8. Calculate delivery days
# --------------------------------------------------

gold_orders_df = gold_orders_df.withColumn(
    "delivery_days",
    datediff(
        col("order_delivered_customer_date"),
        col("order_purchase_timestamp")
    )
)

# --------------------------------------------------
# 9. Calculate delivery delay
# --------------------------------------------------

gold_orders_df = gold_orders_df.withColumn(
    "delivery_delay_days",
    datediff(
        col("order_delivered_customer_date"),
        col("order_estimated_delivery_date")
    )
)

# --------------------------------------------------
# 10. Create delivery status
# --------------------------------------------------

gold_orders_df = gold_orders_df.withColumn(
    "delivery_status",
    when(
        col("order_delivered_customer_date").isNull(),
        "not_delivered"
    ).when(
        col("delivery_delay_days") > 0,
        "delayed"
    ).otherwise(
        "on_time_or_early"
    )
)

# --------------------------------------------------
# 11. Display record count
# --------------------------------------------------

print("\nGold Orders Record Count:", gold_orders_df.count())

print("\nGold Orders Sample:")
gold_orders_df.show(5, truncate=False)

# --------------------------------------------------
# 12. Convert Spark DataFrame to Pandas
# --------------------------------------------------

gold_orders_pandas = gold_orders_df.toPandas()

# --------------------------------------------------
# 13. Convert Pandas DataFrame to Arrow Table
# --------------------------------------------------

gold_orders_table = pa.Table.from_pandas(
    gold_orders_pandas,
    preserve_index=False
)

# --------------------------------------------------
# 14. Remove previous output if it exists
# --------------------------------------------------

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 15. Save Parquet using PyArrow
# --------------------------------------------------

OUTPUT_FILE = OUTPUT_DIR / "gold_orders.parquet"

pq.write_table(
    gold_orders_table,
    OUTPUT_FILE,
    compression="snappy"
)

print("\nGold Orders dataset saved successfully!")
print("Output location:", OUTPUT_FILE)

# --------------------------------------------------
# 16. Stop Spark
# --------------------------------------------------

spark.stop()
