
from pathlib import Path
import duckdb

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
GOLD_DIR = PROJECT_DIR / "data" / "gold"

# 2. Connect to DuckDB
con = duckdb.connect(
    str(PROJECT_DIR / "ecommerce_analytics.duckdb")
)

print("DuckDB connected successfully!")

# 3. Register Gold Parquet files as SQL views
datasets = {
    "gold_orders": "gold_orders/gold_orders.parquet",
    "gold_revenue": "gold_revenue/gold_revenue.parquet",
    "gold_customers": "gold_customers/gold_customers.parquet",
    "gold_products": "gold_products/gold_products.parquet",
    "gold_sellers": "gold_sellers/gold_sellers.parquet",
    "gold_reviews": "gold_reviews/gold_reviews.parquet"
}

for view_name, relative_path in datasets.items():

    file_path = GOLD_DIR / relative_path

    if not file_path.exists():
        raise FileNotFoundError(
            f"Gold dataset not found: {file_path}"
        )

    con.execute(
        f"""
        CREATE OR REPLACE VIEW {view_name} AS
        SELECT * FROM read_parquet('{file_path.as_posix()}')
        """
    )

    print(f"SQL view created: {view_name}")

# 4. Run first SQL query
print("\nTOTAL ORDERS")
print("=" * 50)

result = con.execute("""
    SELECT COUNT(*) AS total_orders
    FROM gold_orders
""").df()

print(result.to_string(index=False))

# 5. Run second SQL query
print("\nORDER STATUS DISTRIBUTION")
print("=" * 50)

result = con.execute("""
    SELECT
        order_status,
        COUNT(*) AS total_orders
    FROM gold_orders
    GROUP BY order_status
    ORDER BY total_orders DESC
""").df()

print(result.to_string(index=False))

# 6. Close DuckDB connection
con.close()

print("\nSQL analytics completed successfully!")
