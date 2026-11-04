
from pathlib import Path
import duckdb

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_DIR / "ecommerce_analytics.duckdb"
SQL_FILE = PROJECT_DIR / "sql" / "01_database_setup.sql"

# 2. Connect to existing DuckDB database
con = duckdb.connect(str(DATABASE_FILE))

print("Connected to DuckDB successfully!")

# 3. Read SQL file
sql_script = SQL_FILE.read_text(encoding="utf-8")

# 4. Execute SQL statements
con.execute(sql_script)

print("Database setup SQL executed successfully!")

# 5. Verify created views
views = con.execute("SHOW TABLES").fetchall()

print("\nAvailable tables and views:")

for view in views:
    print(view[0])

# 6. Close connection
con.close()

print("\nDatabase setup completed!")
