from pathlib import Path
from pyspark.sql import SparkSession

# Find the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Path to Silver Orders Parquet file
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
    .appName("EcommerceDataEngineering")
    .master("local[*]")
    .getOrCreate()
)

# Load Parquet data
orders_df = spark.read.parquet(str(ORDERS_FILE))

# Display results
print("Total number of orders:", orders_df.count())

print("\nOrders Schema:")
orders_df.printSchema()

print("\nFirst 5 Orders:")
orders_df.show(5, truncate=False)

# Stop Spark
spark.stop()