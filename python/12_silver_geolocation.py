
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "olist_geolocation_dataset.csv"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "silver" / "geolocation"
OUTPUT_FILE = OUTPUT_DIR / "geolocation.parquet"

# 2. Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load raw geolocation dataset
geo = pd.read_csv(
    RAW_FILE,
    dtype={"geolocation_zip_code_prefix": "string"}
)

print("Raw geolocation dataset loaded.")
print("Rows before cleaning:", len(geo))

# 4. Clean location text columns
geo["geolocation_city"] = geo["geolocation_city"].str.strip()
geo["geolocation_state"] = (
    geo["geolocation_state"].str.strip().str.upper()
)

# 5. Convert coordinates to numeric values
coordinate_columns = [
    "geolocation_lat",
    "geolocation_lng"
]

for column in coordinate_columns:
    geo[column] = pd.to_numeric(
        geo[column],
        errors="coerce"
    )

# 6. Validate coordinate ranges
invalid_latitude = (
    ~geo["geolocation_lat"].between(-90, 90)
).sum()

invalid_longitude = (
    ~geo["geolocation_lng"].between(-180, 180)
).sum()

print("\nCoordinate validation:")
print("Invalid latitude records:", invalid_latitude)
print("Invalid longitude records:", invalid_longitude)

# 7. Display missing values
print("\nMissing values after cleaning:")
print(geo.isnull().sum())

# 8. Check duplicate ZIP code prefixes
print(
    "\nDuplicate ZIP code prefix records:",
    geo["geolocation_zip_code_prefix"].duplicated().sum()
)

# 9. Preserve all records and save as Parquet
geo.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Geolocation dataset created successfully!")
print("Rows after cleaning:", len(geo))
print("Output file:", OUTPUT_FILE)

print("\nData types after cleaning:")
print(geo.dtypes)
