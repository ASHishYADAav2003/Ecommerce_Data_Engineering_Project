from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, round

# Find project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Reviews Parquet path
REVIEWS_FILE = (
    PROJECT_DIR / "data" / "processed" / "silver"
    / "reviews" / "reviews.parquet"
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("SparkReviewAnalysis")
    .master("local[*]")
    .getOrCreate()
)

# Load reviews
reviews_df = spark.read.parquet(str(REVIEWS_FILE))

# Total reviews
print("\nTotal Reviews:", reviews_df.count())

# Review score distribution
print("\nReview Score Distribution:")

reviews_df.groupBy(
    "review_score"
).agg(
    count("*").alias("total_reviews")
).orderBy(
    "review_score"
).show()

# Average review score
print("\nAverage Review Score:")

reviews_df.select(
    round(avg("review_score"), 2).alias("average_review_score")
).show()

# Review counts by score
print("\nReview Count by Score:")

reviews_df.groupBy(
    "review_score"
).count().orderBy(
    col("count").desc()
).show()

# Stop Spark
spark.stop()