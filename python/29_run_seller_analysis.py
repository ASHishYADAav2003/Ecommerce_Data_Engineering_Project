from pathlib import Path
import duckdb

# Get project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Database and SQL file paths
DATABASE_FILE = PROJECT_DIR / "ecommerce_analytics.duckdb"
SQL_FILE = PROJECT_DIR / "sql" / "06_seller_analysis.sql"

# Connect to DuckDB
con = duckdb.connect(str(DATABASE_FILE))

# Read SQL file
sql_script = SQL_FILE.read_text(encoding="utf-8")

# Execute each SQL query
queries = sql_script.split(";")

for i, query in enumerate(queries, start=1):
    if query.strip():
        print(f"\n========== SELLER ANALYSIS {i} ==========")

        result = con.execute(query).fetchdf()

        print(result.to_string(index=False))

# Close connection
con.close()

print("\nSeller analysis completed successfully!")