
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

report_path = REPORT_DIR / "dataset_summary.txt"

with open(report_path, "w", encoding="utf-8") as report:

    report.write("OLIST E-COMMERCE DATASET SUMMARY\n")
    report.write("=" * 60 + "\n\n")

    total_rows = 0

    for file_path in csv_files:
        df = pd.read_csv(file_path)

        total_rows += len(df)

        report.write(f"File: {file_path.name}\n")
        report.write(f"Rows: {df.shape[0]}\n")
        report.write(f"Columns: {df.shape[1]}\n")
        report.write(f"Column names: {', '.join(df.columns)}\n")

        report.write("\nMissing values:\n")
        report.write(df.isnull().sum().to_string())

        report.write("\n\n" + "-" * 60 + "\n\n")

    report.write(f"\nTotal CSV files: {len(csv_files)}\n")
    report.write(f"Total rows across files: {total_rows}\n")

print(f"Report successfully created: {report_path}")
print(f"CSV files analysed: {len(csv_files)}")
print(f"Total rows across files: {total_rows}")
