
from pathlib import Path
import pandas as pd

# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "product_category_name_translation.csv"
)

OUTPUT_DIR = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "silver"
    / "category_translation"
)

OUTPUT_FILE = OUTPUT_DIR / "category_translation.parquet"

# 2. Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Load raw category translation dataset
categories = pd.read_csv(RAW_FILE)

print("Raw category translation dataset loaded.")
print("Rows before cleaning:", len(categories))

# 4. Clean text columns
text_columns = [
    "product_category_name",
    "product_category_name_english"
]

for column in text_columns:
    categories[column] = categories[column].str.strip()

# 5. Validate required columns
for column in text_columns:
    if categories[column].isnull().any():
        raise ValueError(f"Missing values found in {column}!")

# 6. Validate Portuguese category key
if categories["product_category_name"].duplicated().any():
    raise ValueError("Duplicate Portuguese category names found!")

# 7. Check English translations
if categories["product_category_name_english"].duplicated().any():
    print(
        "Note: Some English translations are shared by multiple "
        "Portuguese categories."
    )

# 8. Display category information
print("\nNumber of Portuguese categories:",
      categories["product_category_name"].nunique())

print("Number of English categories:",
      categories["product_category_name_english"].nunique())

print("\nFirst 10 category mappings:")
print(categories.head(10).to_string(index=False))

# 9. Save as Parquet
categories.to_parquet(OUTPUT_FILE, index=False)

print("\nSilver Category Translation dataset created successfully!")
print("Rows after cleaning:", len(categories))
print("Output file:", OUTPUT_FILE)
