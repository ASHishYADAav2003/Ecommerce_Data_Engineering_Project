# E-Commerce Data Engineering Pipeline

A beginner-friendly end-to-end data engineering project using the
Brazilian E-Commerce Public Dataset by Olist. It demonstrates raw-data
exploration, data-quality checks, Silver and Gold Parquet
transformations, DuckDB and SQL analytics, PySpark processing, AWS S3
storage, Glue Data Catalog, Athena queries, and a Streamlit dashboard
with a simple AI Business Assistant.

> This guide documents the project state and scripts used during
> development. Check your local files and AWS console before assuming
> that a resource or output exists.

## 1. Project overview

**Dataset:** [Brazilian E-Commerce Public Dataset by
Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The nine source CSVs are:

-   `olist_customers_dataset.csv`
-   `olist_geolocation_dataset.csv`
-   `olist_order_items_dataset.csv`
-   `olist_order_payments_dataset.csv`
-   `olist_order_reviews_dataset.csv`
-   `olist_orders_dataset.csv`
-   `olist_products_dataset.csv`
-   `olist_sellers_dataset.csv`
-   `product_category_name_translation.csv`

**Technology stack**

  -----------------------------------------------------------------------
  Technology                          Role
  ----------------------------------- -----------------------------------
  Python, Pandas, NumPy               Data exploration, quality checks
                                      and transformations

  CSV and Parquet                     Raw and processed data formats

  DuckDB                              Local analytical database and
                                      Parquet SQL views

  SQL                                 Business analysis

  PySpark                             Spark-based data processing and
                                      analysis

  Amazon S3                           Cloud storage for Gold Parquet
                                      files

  AWS Glue Data Catalog               Database and table metadata

  Amazon Athena                       SQL queries over S3 Parquet data

  Streamlit                           Interactive dashboard

  Ollama API + OpenAI Python client   Simple conversational answer
                                      generation
  -----------------------------------------------------------------------

## 2. Project folder structure

``` text
Ecommerce_Data_Engineering_Project/
├── data/
│   ├── raw/                         # Original Olist CSV files
│   ├── processed/silver/            # Cleaned Silver Parquet datasets
│   └── gold/                        # Business-ready Python and Spark Gold data
├── python/                          # Exploration, quality, Silver, Gold and SQL runners
├── sql/                             # DuckDB setup and analytics queries
├── pyspark/                         # PySpark analysis and Spark Gold scripts
├── aws/                             # AWS notes/scripts, if maintained locally
├── reports/                         # Dataset and data-quality reports
├── app.py                           # Streamlit dashboard and AI assistant
├── ecommerce_analytics.duckdb       # Generated local DuckDB database
├── .env                             # API credentials; never commit
├── .gitignore
├── requirements.txt
└── README.md                         # This guide
```

The raw, processed and Gold data folders, virtual environment, `.env`
and local database should be excluded from Git where appropriate. The
source scripts, SQL and documentation should be committed.

## 3. Windows setup

The development project folder is:

``` text
C:\Users\Ashish yadav\OneDrive\Desktop\Ecommerce_Data_Engineering_Project
```

Open this folder in VS Code. Use **Terminal → New Terminal**.

### Activate the existing virtual environment

``` powershell
.\ecom_venv\Scripts\Activate.ps1
```

If the environment does not exist, create it first:

``` powershell
python -m venv ecom_venv
.\ecom_venv\Scripts\Activate.ps1
```

Install dependencies from the project root:

``` powershell
python -m pip install -r requirements.txt
```

If you are setting up the packages individually:

``` powershell
python -m pip install pandas numpy matplotlib pyarrow duckdb pyspark streamlit python-dotenv openai
```

PySpark also needs Java. The development environment used OpenJDK 17.

Check versions:

``` powershell
python --version
java -version
python -m streamlit --version
```

## 4. Download and place the source data

1.  Download and extract the Olist dataset from the Kaggle link above.
2.  Place all nine original CSVs in `data/raw/`.
3.  Confirm the filenames match the list in Section 1.
4.  Keep the original CSVs unchanged. Transformations should write new
    files to Silver and Gold folders.

## 5. Understand the data relationships

  Related datasets                    Join key
  ----------------------------------- -------------------------
  Customers and Orders                `customer_id`
  Orders and Order Items              `order_id`
  Orders and Payments                 `order_id`
  Orders and Reviews                  `order_id`
  Products and Order Items            `product_id`
  Sellers and Order Items             `seller_id`
  Products and Category Translation   `product_category_name`

Important modeling details:

-   `customer_id` identifies the customer record associated with an
    order.
-   `customer_unique_id` identifies a customer across potentially
    multiple customer records. Use it for true repeat-customer analysis.
-   Source `review_id` values are repeated. The investigation found
    repeated IDs associated with different orders, so do not delete
    records based on `review_id` alone. `(review_id, order_id)` is the
    candidate composite key used for validation.
-   Geolocation postal-code prefixes can repeat. Do not remove them
    without a deliberate aggregation strategy.
-   The category translation file maps Portuguese category names to
    English names.

## 6. End-to-end data workflow

``` text
Olist CSV files
      |
      v
Raw layer (data/raw)
      |
      v
Exploration and data-quality checks
      |
      v
Silver Parquet layer
      |
      v
Gold Parquet layer
      |
      +--------------------------+
      |                          |
      v                          v
DuckDB + SQL analytics       PySpark analysis
      |                          |
      +------------+-------------+
                   |
                   v
            Streamlit app

Gold Parquet files
      |
      v
Amazon S3
      |
      v
Glue Data Catalog
      |
      v
Amazon Athena
```

### 6.1 Exploration and quality checks

Run these from the project root, with `ecom_venv` activated:

``` powershell
python python/01_data_exploration.py
python python/02_generate_dataset_report.py
python python/03_data_quality_check.py
python python/04_investigate_duplicate_reviews.py
```

Purpose:

-   Inspect row counts, columns, data types, missing values and sample
    records.
-   Generate `reports/dataset_summary.txt`.
-   Generate `reports/data_quality_report.csv`.
-   Investigate duplicate review IDs without discarding legitimate
    review records.

The checks performed during development found no orphan records in the
tested relationships. The review dataset contained duplicate `review_id`
values; therefore a single-column uniqueness assumption is unsafe.

### 6.2 Silver layer

Silver contains cleaned/standardized Parquet versions of the nine source
datasets.

``` powershell
python python/05_silver_customers.py
python python/06_silver_orders.py
python python/07_silver_order_items.py
python python/08_silver_payments.py
python python/09_silver_reviews.py
python python/10_silver_products.py
python python/11_silver_sellers.py
python python/12_silver_geolocation.py
python python/13_silver_category_translation.py
python python/14_validate_silver_layer.py
```

Expected output files:

``` text
data/processed/silver/customers/customers.parquet
data/processed/silver/orders/orders.parquet
data/processed/silver/order_items/order_items.parquet
data/processed/silver/payments/payments.parquet
data/processed/silver/reviews/reviews.parquet
data/processed/silver/products/products.parquet
data/processed/silver/sellers/sellers.parquet
data/processed/silver/geolocation/geolocation.parquet
data/processed/silver/category_translation/category_translation.parquet
```

Run the validation script after generating all nine datasets.

### 6.3 Python Gold layer

Gold contains business-oriented datasets built from Silver.

``` powershell
python python/15_gold_orders.py
python python/16_gold_revenue.py
python python/17_gold_customers.py
python python/18_gold_products.py
python python/19_gold_sellers.py
python python/20_gold_reviews.py
python python/21_validate_gold_layer.py
```

Expected output files:

``` text
data/gold/gold_orders/gold_orders.parquet
data/gold/gold_revenue/gold_revenue.parquet
data/gold/gold_customers/gold_customers.parquet
data/gold/gold_products/gold_products.parquet
data/gold/gold_sellers/gold_sellers.parquet
data/gold/gold_reviews/gold_reviews.parquet
```

Gold dataset grain and purpose:

  -----------------------------------------------------------------------------
  Dataset                 Grain / key                   Purpose
  ----------------------- ----------------------------- -----------------------
  Gold Orders             One row per `order_id`        Order, customer and
                                                        delivery metrics

  Gold Revenue            One row per                   Item revenue, freight
                          `(order_id, order_item_id)`   and category analysis

  Gold Customers          One row per `customer_id`     Customer-level order
                                                        and spending metrics

  Gold Products           One row per `product_id`      Product and category
                                                        sales metrics

  Gold Sellers            One row per `seller_id`       Seller performance

  Gold Reviews            One row per                   Review scores and
                          `(review_id, order_id)`       response analysis
  -----------------------------------------------------------------------------

Expected row counts for the Olist dataset used during development:

  Dataset               Rows
  ---------------- ---------
  Gold Orders         99,441
  Gold Revenue       112,650
  Gold Customers      99,441
  Gold Products       32,951
  Gold Sellers         3,095
  Gold Reviews        99,224

These are reference counts; they can differ if the input files differ.

**Metric cautions:** Gold Revenue is based on order-item price and
freight values. Treat it as gross order-item value for this project, not
recognized accounting revenue. Gold Customers is grouped by
`customer_id`; use `customer_unique_id` to calculate repeat customers
across customer records.

## 7. DuckDB and SQL analytics

DuckDB creates a local analytical database and can query Parquet files
directly.

The setup SQL file is:

``` text
sql/01_database_setup.sql
```

It creates views over the six Python Gold Parquet files using DuckDB
`read_parquet(...)`.

Python setup/runner scripts:

``` powershell
python python/22_run_sql_analytics.py
python python/24_execute_sql_file.py
```

The local database is `ecommerce_analytics.duckdb`. It is generated
locally and should not be committed.

SQL analysis files:

  -----------------------------------------------------------------------
  File                                Topics
  ----------------------------------- -----------------------------------
  `sql/02_order_analysis.sql`         Order count, status, delivery and
                                      state analysis

  `sql/03_revenue_analysis.sql`       Item revenue, freight, monthly
                                      revenue, categories and average
                                      order value

  `sql/04_customer_analysis.sql`      Customer records, spending and
                                      customer analysis

  `sql/05_product_analysis.sql`       Product revenue, units, category
                                      price and products without sales

  `sql/06_seller_analysis.sql`        Seller performance

  `sql/07_review_analysis.sql`        Review scores and response analysis

  `sql/08_business_overview.sql`      Consolidated business overview
  -----------------------------------------------------------------------

Run the Python analysis runners:

``` powershell
python python/25_run_order_analysis.py
python python/26_run_revenue_analysis.py
python python/27_run_customer_analysis.py
python python/28_run_product_analysis.py
python python/29_run_seller_analysis.py
python python/30_run_review_analysis.py
python python/31_run_business_overview.py
```

Run from the project root so relative file paths resolve correctly.

## 8. PySpark

PySpark scripts demonstrate Spark-based reading, analysis, joins and
Gold transformations. Java 17 was used during development.

Analysis scripts:

``` powershell
python pyspark/01_spark_read_orders.py
python pyspark/02_spark_order_analysis.py
python pyspark/03_spark_product_analysis.py
python pyspark/04_spark_customer_analysis.py
python pyspark/05_spark_revenue_analysis.py
python pyspark/06_spark_seller_analysis.py
python pyspark/07_spark_review_analysis.py
python pyspark/08_spark_order_customer_join.py
python pyspark/09_spark_category_analysis.py
python pyspark/10_spark_delivery_analysis.py
```

Spark Gold scripts:

``` powershell
python pyspark/11_spark_gold_orders.py
python pyspark/12_spark_gold_revenue.py
python pyspark/13_spark_gold_customers.py
python pyspark/14_spark_gold_products.py
python pyspark/15_spark_validate_gold.py
```

Spark Gold outputs are separate from Python Gold outputs:

``` text
data/gold/spark_gold_orders/gold_orders.parquet
data/gold/spark_gold_revenue/gold_revenue.parquet
data/gold/spark_gold_customers/gold_customers.parquet
data/gold/spark_gold_products/gold_products.parquet
```

**Windows implementation note:** Spark's Hadoop-based Parquet writer
raised a winutils/Hadoop dependency issue in this environment. The Spark
Gold scripts use `toPandas()` and PyArrow to write Parquet instead. This
avoids installing Hadoop/winutils for this project, but it requires the
resulting data to fit in local memory and is not a large-scale
distributed write strategy.

## 9. AWS cloud workflow

The cloud workflow used during development:

1.  Create a private S3 bucket.
2.  Keep S3 Block Public Access enabled.
3.  Upload the six Python Gold Parquet files into their own prefixes.
4.  Create a Glue Data Catalog database manually.
5.  Create Athena external tables over the Parquet files.
6.  Query the tables in Athena.

Development resource names:

-   S3 bucket: `ecommerce-data-pipeline-01`
-   Glue database: `ecommerce_analytics_db`
-   Region: `ap-south-1` (Asia Pacific - Mumbai)

S3 prefixes:

``` text
gold_orders/
gold_revenue/
gold_customers/
gold_products/
gold_sellers/
gold_reviews/
```

Example object path:

``` text
s3://ecommerce-data-pipeline-01/gold_orders/gold_orders.parquet
```

Use the matching prefix and filename for each of the other five
datasets.

### Athena setup

Athena needs an S3 query-results location configured in the workgroup. A
prefix such as `athena-results/` may be used; verify the actual setting
in the AWS console.

Create six external tables in `ecommerce_analytics_db`, each pointing to
its matching S3 prefix and using Parquet storage. A Glue crawler was not
used in this workflow; tables were created manually because crawler
creation was not available in the account setup.

Schema lessons from this project:

-   Athena column types must match the actual Parquet schema.
-   Gold Orders `delivery_days` and `delivery_delay_days` were `DOUBLE`.
-   Gold Customers `customer_zip_code_prefix` was mapped to Athena
    `STRING`.
-   Gold Products `product_name_lenght`, `product_description_lenght`,
    and `product_photos_qty` were `DOUBLE`.
-   If Athena reports a Parquet schema mismatch, inspect the actual
    Parquet schema and correct the table definition instead of guessing.

**Cost/security:** Athena charges based on data scanned. AWS free-tier
and credit eligibility depends on current account terms and usage. Keep
S3 private and never commit AWS credentials or API keys.

## 10. Streamlit dashboard and AI Business Assistant

The app is in the project root:

``` text
app.py
```

The app has two sections:

1.  **Business Dashboard** --- business KPIs and charts sourced from
    DuckDB and local Gold Parquet data.
2.  **AI Business Assistant** --- a simple conversational assistant
    using an Ollama API model.

The assistant is an answer-generating chatbot. It is not a SQL agent,
RAG system, or database-connected chatbot. Do not assume it can read
dashboard metrics or query DuckDB.

### Configure `.env`

Create `.env` in the project root. Do not commit it.

``` dotenv
OLLAMA_API_KEY=your_actual_api_key
OLLAMA_MODEL=your_actual_model_name
OLLAMA_BASE_URL=https://ollama.com/v1
```

Use the exact model identifier and API base URL supported by your Ollama
account. Never share the API key in screenshots, chat, source code or
GitHub.

### Run Streamlit

Activate `ecom_venv`, then run from the project root:

``` powershell
python -m streamlit run app.py
```

Open the local URL printed in the terminal, commonly:

``` text
http://localhost:8501
```

### Common errors

**`ModuleNotFoundError: No module named 'openai'`**

``` powershell
python -m pip install openai
```

**`ModuleNotFoundError: No module named 'dotenv'`**

``` powershell
python -m pip install python-dotenv
```

Install into the same activated environment used to launch Streamlit.

**Dashboard cannot find a Gold Parquet file or DuckDB view**

-   Confirm the terminal is in the project root.
-   Confirm the six Python Gold Parquet files exist under `data/gold/`.
-   Run the Gold scripts and DuckDB setup scripts if needed.
-   Check the paths referenced by `app.py`.

**AI assistant API error**

-   Confirm `.env` exists in the project root.
-   Check environment-variable names, model identifier and API base URL
    against current provider documentation.
-   Restart Streamlit after changing `.env`.
-   Do not paste the API key into logs or screenshots.

## 11. Git and GitHub

The `.gitignore` should exclude `.env`, virtual environments, Python
caches, local DuckDB files, raw/processed/Gold datasets, Spark temporary
folders and Streamlit secrets.

Keep the source code, SQL, README and requirements file in Git.

Before committing, run:

``` powershell
git status
```

Check that `.env`, `ecom_venv/`, the DuckDB database and large data
files are not staged.

Basic first-time workflow:

``` powershell
git init
git add .
git status
git commit -m "Initial commit: e-commerce data engineering pipeline"
```

Create an empty GitHub repository and follow GitHub's instructions to
add the remote and push. Do not push until you have reviewed the staged
files.

If `.env` was committed previously, `.gitignore` alone does not erase it
from Git history. Remove it from tracking and rotate the exposed API
key.

## 12. Full local rebuild order

To reproduce the project from the original CSVs:

1.  Place all nine CSVs in `data/raw/`.
2.  Activate `ecom_venv`.
3.  Run Python exploration and quality scripts `01` to `04`.
4.  Run Silver scripts `05` to `14`.
5.  Run Python Gold scripts `15` to `21`.
6.  Create DuckDB views and run SQL setup/analysis scripts.
7.  Run PySpark analysis and Spark Gold scripts if you want to reproduce
    the Spark branch.
8.  Configure `.env`, ensure local Gold data and DuckDB views exist, and
    launch Streamlit.
9.  For AWS, upload the six Python Gold Parquet files, then ensure
    Glue/Athena tables point to the correct S3 prefixes.

Run each layer's validation script before proceeding to the next layer.

## 13. Known limitations and interpretation

-   This is a historical public dataset, not a live e-commerce feed.
-   Gold Revenue is a gross order-item value measure for analysis, not a
    formal accounting revenue measure.
-   Gold Customers is grouped by `customer_id`; true repeat-customer
    analysis should use `customer_unique_id`.
-   Review IDs repeat in the source; preserve records and use the
    composite key where appropriate.
-   Geolocation postal prefixes repeat and need a deliberate aggregation
    strategy.
-   Spark Gold uses Pandas/PyArrow output to avoid the Windows Hadoop
    writer dependency; this is not ideal for very large datasets.
-   The AI assistant is not connected to the business database.
-   AWS costs depend on account eligibility, region, services used and
    data scanned.

## 14. Suggested project presentation walkthrough

Use this order when explaining the project:

1.  **Business problem:** E-commerce information is distributed across
    multiple source files and needs reliable business-ready datasets.
2.  **Source data:** Introduce the nine Olist CSV files and their
    relationships.
3.  **Data quality:** Show missing-value, duplicate-key and
    referential-integrity checks. Explain why duplicate review IDs were
    not blindly removed.
4.  **Silver layer:** Explain standardization and Parquet outputs.
5.  **Gold layer:** Explain the grain and business purpose of each of
    the six datasets.
6.  **DuckDB and SQL:** Demonstrate local views and business questions
    answered with SQL.
7.  **PySpark:** Explain Spark reading, joins, aggregations and separate
    Spark Gold outputs.
8.  **AWS:** Show private S3 storage, Glue Data Catalog and Athena
    queries.
9.  **Streamlit:** Demonstrate the dashboard and explain its local
    DuckDB/Gold data source.
10. **AI assistant:** Demonstrate answer generation and clarify that it
    is not a database-querying assistant.

## 15. Completion checklist

-   [ ] Downloaded the Olist dataset and placed all nine CSVs in
    `data/raw/`.
-   [ ] Activated the Python virtual environment.
-   [ ] Ran exploration and generated the dataset summary.
-   [ ] Ran data-quality checks and investigated duplicate review IDs.
-   [ ] Generated all nine Silver Parquet datasets.
-   [ ] Validated the Silver layer.
-   [ ] Generated all six Python Gold Parquet datasets.
-   [ ] Validated the Gold layer.
-   [ ] Created DuckDB views over Gold Parquet files.
-   [ ] Ran SQL analysis scripts.
-   [ ] Ran PySpark analysis scripts.
-   [ ] Generated and validated the four Spark Gold datasets.
-   [ ] Uploaded six Python Gold Parquet files to private S3 prefixes.
-   [ ] Created the Glue database and Athena tables.
-   [ ] Ran Athena validation and business overview queries.
-   [ ] Ran the Streamlit dashboard locally.
-   [ ] Tested the AI Business Assistant without exposing its API key.
-   [ ] Checked `.gitignore` and verified `.env` is not staged.
-   [ ] Reviewed Git status before committing and pushing to GitHub.

## 16. Key project paths

``` text
Project root:
C:\Users\Ashish yadav\OneDrive\Desktop\Ecommerce_Data_Engineering_Project

Raw CSVs:
data/raw/

Silver Parquet:
data/processed/silver/

Python Gold Parquet:
data/gold/

SQL:
sql/

PySpark:
pyspark/

Streamlit application:
app.py

DuckDB database:
ecommerce_analytics.duckdb

Private API configuration:
.env
```

Keep `.env` private. Use this README as the main navigation document
when running, validating, understanding or presenting the project.
