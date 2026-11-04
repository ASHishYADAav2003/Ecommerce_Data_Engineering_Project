from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

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
    .appName("SparkOrderCustomerJoin")
    .master("local[*]")
    .getOrCreate()
)

# Load datasets
orders_df = spark.read.parquet(str(ORDERS_FILE))
customers_df = spark.read.parquet(str(CUSTOMERS_FILE))

# Select customer columns
customers_selected_df = customers_df.select(
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state"
)

# Join orders with customers
order_customer_df = orders_df.join(
    customers_selected_df,
    on="customer_id",
    how="inner"
)

# Display total joined records
print(
    "\nTotal Joined Records:",
    order_customer_df.count()
)

# Display selected columns
print("\nJoined Order and Customer Data:")

order_customer_df.select(
    "order_id",
    "customer_id",
    "customer_unique_id",
    "order_status",
    "customer_city",
    "customer_state"
).show(10, truncate=False)

# Display orders by customer state
print("\nOrders by Customer State:")

order_customer_df.groupBy(
    "customer_state"
).count().orderBy(
    col("count").desc()
).show()

# Stop Spark
spark.stop()