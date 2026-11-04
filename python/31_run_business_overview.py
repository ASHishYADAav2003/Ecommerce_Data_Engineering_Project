from pathlib import Path
import duckdb

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_DIR / "ecommerce_analytics.duckdb"
SQL_FILE = PROJECT_DIR / "sql" / "08_business_overview.sql"

con = duckdb.connect(str(DATABASE_FILE))

sql_script = SQL_FILE.read_text(encoding="utf-8")

queries = sql_script.split(";")

for i, query in enumerate(queries, start=1):
    if query.strip():
        print(f"\n========== BUSINESS OVERVIEW {i} ==========")

        result = con.execute(query).fetchdf()

        print(result.to_string(index=False))

con.close()

print("\nBusiness overview completed successfully!")