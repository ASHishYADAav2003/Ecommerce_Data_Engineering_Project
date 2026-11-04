

from pathlib import Path
import duckdb

# 1. Define paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
GOLD_DIR = PROJECT_DIR / "data" / "gold"

# 2. Connect to DuckDB
con = duckdb.connect(
    str(PROJECT_DIR / "ecommerce_analytics.duckdb")
)

# 3. Register Gold Orders view
orders_file = GOLD_DIR / "gold_orders" / "gold_orders.parquet"

con.execute(f"""
    CREATE OR REPLACE VIEW gold_orders AS
    SELECT * FROM read_parquet('{orders_file.as_posix()}')
""")

# 4. Read SQL file
sql_file = PROJECT_DIR / "sql" / "02_order_analysis.sql"

sql_queries = sql_file.read_text(encoding="utf-8")

# 5. Execute each query separately
queries = [
    query.strip()
    for query in sql_queries.split(";")
    if query.strip()
]

for index, query in enumerate(queries, start=1):

    print(f"\nQUERY {index} RESULT")
    print("=" * 50)

    result = con.execute(query).df()
    print(result.to_string(index=False))

# 6. Close connection
con.close()

print("\nOrder analysis completed successfully!")
