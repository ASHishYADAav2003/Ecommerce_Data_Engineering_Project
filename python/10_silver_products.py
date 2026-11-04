
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "olist_products_dataset.csv"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "silver" / "products"
OUTPUT_FILE = OUTPUT_DIR / "products.parquet"

# 2. Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load raw products dataset
products = pd.read_csv(RAW_FILE)

print("Raw products dataset loaded.")
print("Rows before cleaning:", len(products))

# 4. Clean text columns
products["product_id"] = products["product_id"].str.strip()

products["product_category_name"] = (
    products["product_category_name"].str.strip()
)

# 5. Convert numeric columns
numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for column in numeric_columns:
    products[column] = pd.to_numeric(
        products[column],
        errors="coerce"
    )

# 6. Validate product IDs
if products["product_id"].isnull().any():
    raise ValueError("Missing product_id values found!")

if products["product_id"].duplicated().any():
    raise ValueError("Duplicate product_id values found!")

# 7. Validate numeric product attributes
for column in numeric_columns:
    invalid_values = (products[column] < 0).sum()

    if invalid_values > 0:
        raise ValueError(
            f"Negative values found in {column}: {invalid_values}"
        )

# 8. Report missing values
print("\nMissing values after cleaning:")
print(products.isnull().sum())

# 9. Save as Parquet
products.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Products dataset created successfully!")
print("Rows after cleaning:", len(products))
print("Output file:", OUTPUT_FILE)

print("\nData types after cleaning:")
print(products.dtypes)
