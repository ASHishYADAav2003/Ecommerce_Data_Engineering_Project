
from pathlib import Path
import duckdb

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_DIR / "ecommerce_analytics.duckdb"
SQL_FILE = PROJECT_DIR / "sql" / "02_order_analysis.sql"

# 2. Connect to existing database
con = duckdb.connect(str(DATABASE_FILE))

print("Connected to DuckDB successfully!")

# 3. Read SQL file
sql_script = SQL_FILE.read_text(encoding="utf-8")

# 4. Split SQL file into individual queries
queries = [
    query.strip()
    for query in sql_script.split(";")
    if query.strip()
]

# 5. Execute each query
for index, query in enumerate(queries, start=1):

    print(f"\nQUERY {index} RESULT")
    print("=" * 50)

    result = con.execute(query).df()

    print(result.to_string(index=False))

# 6. Close database connection
con.close()

print("\nOrder analysis completed successfully!")
