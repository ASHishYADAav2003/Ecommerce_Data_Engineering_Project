# E-Commerce Data Engineering Pipeline --- Master Project Guide

**Purpose:** Use this document as the map for the whole project. It
explains the architecture, folders, file purposes, execution order, data
relationships, important caveats, current status, and planned AWS stage.

**Project root:**
`C:\Users\Ashish yadav\OneDrive\Desktop\Ecommerce_Data_Engineering_Project`

**Environment:** Windows 11, VS Code, PowerShell, Python virtual
environment `ecom_venv`, Java 17 (Temurin), PySpark, PyArrow, DuckDB.

------------------------------------------------------------------------

## 1. Project overview

This project uses the Brazilian E-Commerce Public Dataset by Olist
(Kaggle): https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains anonymized Brazilian e-commerce activity, mainly
from 2016--2018, across nine CSV files. The dataset was identified
during the project as CC BY-NC-SA 4.0. Keep attribution and check the
current license terms before publishing or commercial use.

### Pipeline architecture

``` text
9 original CSV files
       |
       v
RAW (data/raw/)
       |
       v
Explore data + quality checks (Python)
       |
       v
SILVER (data/processed/silver/)
9 cleaned and standardized Parquet datasets
       |
       v
GOLD (data/gold/)
6 Python Gold outputs + 4 separate Spark Gold outputs
       |
       +----------------------+----------------------+
       |                                             |
       v                                             v
DuckDB + SQL analytics                         PySpark analysis
       |                                             |
       +----------------------+----------------------+
                              |
                              v
                  PLANNED AWS CLOUD STAGE
                     S3 -> Glue -> Athena
```

-   **Raw:** original source files; keep unchanged.
-   **Silver:** cleaned, standardized Parquet datasets.
-   **Gold:** business-oriented datasets for analysis.
-   **Analytics:** SQL and Spark queries.
-   **AWS (planned):** cloud storage, catalog and SQL querying.

## 2. Folder structure

``` text
Ecommerce_Data_Engineering_Project/
|-- data/
|   |-- raw/                         # 9 original CSV files
|   |-- processed/
|   |   |-- silver/
|   |       |-- customers/
|   |       |-- orders/
|   |       |-- order_items/
|   |       |-- payments/
|   |       |-- reviews/
|   |       |-- products/
|   |       |-- sellers/
|   |       |-- geolocation/
|   |       |-- category_translation/
|   |-- gold/
|       |-- gold_orders/             # Python Gold
|       |-- gold_revenue/
|       |-- gold_customers/
|       |-- gold_products/
|       |-- gold_sellers/
|       |-- gold_reviews/
|       |-- spark_gold_orders/       # Separate Spark Gold
|       |-- spark_gold_revenue/
|       |-- spark_gold_customers/
|       |-- spark_gold_products/
|-- python/                          # Python ETL, checks and SQL runners
|-- sql/                              # DuckDB SQL setup and analysis
|-- pyspark/                          # Spark learning and Gold scripts
|-- aws/                              # planned AWS work
|-- reports/                          # generated reports
|-- dashboard/                        # planned dashboard work
|-- ecommerce_analytics.duckdb        # local DuckDB database
```

There are **10 Gold folders** because there are six original Python Gold
datasets plus four additional Spark Gold implementations. They are
separate outputs. Do not delete the original six or confuse the two
sets.

## 3. Raw datasets and relationships

  -------------------------------------------------------------------------------------------
  CSV                                       Contents                Important key /
                                                                    relationship
  ----------------------------------------- ----------------------- -------------------------
  `olist_customers_dataset.csv`             Customer record and     `customer_id`;
                                            location                `customer_unique_id`
                                                                    identifies a customer
                                                                    across records

  `olist_geolocation_dataset.csv`           ZIP-prefix geolocation  ZIP code prefix
                                            data                    

  `olist_order_items_dataset.csv`           Items, products,        `order_id`,
                                            sellers, price and      `order_item_id`,
                                            freight                 `product_id`, `seller_id`

  `olist_order_payments_dataset.csv`        Payment type,           `order_id`
                                            installments and amount 

  `olist_order_reviews_dataset.csv`         Review score, comments  `order_id`, `review_id`
                                            and timestamps          

  `olist_orders_dataset.csv`                Order status and        `order_id`, `customer_id`
                                            lifecycle timestamps    

  `olist_products_dataset.csv`              Product attributes and  `product_id`,
                                            Portuguese category     `product_category_name`

  `olist_sellers_dataset.csv`               Seller records and      `seller_id`
                                            location                

  `product_category_name_translation.csv`   Portuguese-to-English   `product_category_name`
                                            category mapping        
  -------------------------------------------------------------------------------------------

Relationships: - Customers to Orders: `customer_id` - Orders to Order
Items: `order_id` - Orders to Payments: `order_id` - Orders to Reviews:
`order_id` - Order Items to Products: `product_id` - Order Items to
Sellers: `seller_id` - Products to Category Translation:
`product_category_name`

**Customer identity:** `customer_id` is the order-associated customer
record. `customer_unique_id` helps identify the same real customer
across multiple orders.

## 4. Python files --- inventory and purpose

The scripts are small focused tasks. You are not expected to memorize
every line. Learn each stage's purpose.

### Exploration and quality

  ---------------------------------------------------------------------------
  File                                    Purpose / output
  --------------------------------------- -----------------------------------
  `01_data_exploration.py`                Inspects all nine CSVs: row counts,
                                          columns, types, missing values and
                                          sample rows

  `02_generate_dataset_report.py`         Creates
                                          `reports/dataset_summary.txt`

  `03_data_quality_check.py`              Checks missing IDs, duplicate keys
                                          and referential integrity; creates
                                          `reports/data_quality_report.csv`

  `04_investigate_duplicate_reviews.py`   Investigates repeated review IDs
                                          and composite-key behavior
  ---------------------------------------------------------------------------

### Silver transformations

  -----------------------------------------------------------------------------------------------------------------
  File                                  Output
  ------------------------------------- ---------------------------------------------------------------------------
  `05_silver_customers.py`              `data/processed/silver/customers/customers.parquet`

  `06_silver_orders.py`                 `data/processed/silver/orders/orders.parquet`

  `07_silver_order_items.py`            `data/processed/silver/order_items/order_items.parquet`

  `08_silver_payments.py`               `data/processed/silver/payments/payments.parquet`

  `09_silver_reviews.py`                `data/processed/silver/reviews/reviews.parquet`

  `10_silver_products.py`               `data/processed/silver/products/products.parquet`

  `11_silver_sellers.py`                `data/processed/silver/sellers/sellers.parquet`

  `12_silver_geolocation.py`            `data/processed/silver/geolocation/geolocation.parquet`

  `13_silver_category_translation.py`   `data/processed/silver/category_translation/category_translation.parquet`

  `14_validate_silver_layer.py`         Validates the nine Silver outputs
  -----------------------------------------------------------------------------------------------------------------

### Original Python Gold transformations

  -----------------------------------------------------------------------------------
  File                                Output / purpose
  ----------------------------------- -----------------------------------------------
  `15_gold_orders.py`                 `gold/gold_orders/gold_orders.parquet`; one row
                                      per order, with customer and delivery details

  `16_gold_revenue.py`                `gold/gold_revenue/gold_revenue.parquet`; one
                                      row per order item, with product/category and
                                      item value

  `17_gold_customers.py`              `gold/gold_customers/gold_customers.parquet`;
                                      customer-record-level metrics

  `18_gold_products.py`               `gold/gold_products/gold_products.parquet`;
                                      product metrics, including products without
                                      sales

  `19_gold_sellers.py`                `gold/gold_sellers/gold_sellers.parquet`;
                                      seller metrics

  `20_gold_reviews.py`                `gold/gold_reviews/gold_reviews.parquet`;
                                      reviews enriched with order information

  `21_validate_gold_layer.py`         Validates original Python Gold datasets
  -----------------------------------------------------------------------------------

### DuckDB and SQL runner scripts

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `22_run_sql_analytics.py`           Connects to
                                      `ecommerce_analytics.duckdb` and
                                      registers views over Gold Parquet
                                      files

  `24_execute_sql_file.py`            Executes
                                      `sql/01_database_setup.sql` to
                                      create/refresh views

  `25_run_order_analysis.py`          Runs `sql/02_order_analysis.sql`

  `26_run_revenue_analysis.py`        Runs `sql/03_revenue_analysis.sql`

  `27_run_customer_analysis.py`       Runs `sql/04_customer_analysis.sql`

  `28_run_product_analysis.py`        Runs `sql/05_product_analysis.sql`

  `29_run_seller_analysis.py`         Runs `sql/06_seller_analysis.sql`

  `30_run_review_analysis.py`         Runs `sql/07_review_analysis.sql`

  `31_run_business_overview.py`       Runs `sql/08_business_overview.sql`
  -----------------------------------------------------------------------

**Numbering note:** The project history does not document a `23_...`
Python file. Do not create one just to fill the gap. If one exists
locally, inspect it and add its real purpose to this guide.

## 5. SQL files --- inventory and purpose

  -----------------------------------------------------------------------
  File                                Business questions
  ----------------------------------- -----------------------------------
  `01_database_setup.sql`             Creates six DuckDB views over the
                                      original Python Gold Parquet
                                      datasets

  `02_order_analysis.sql`             Order counts, status distribution,
                                      delivery status/duration and orders
                                      by state

  `03_revenue_analysis.sql`           Item value, freight, monthly
                                      revenue, category revenue and
                                      average order value

  `04_customer_analysis.sql`          Customer counts, spending and
                                      customer-state summaries

  `05_product_analysis.sql`           Product counts, top products,
                                      category revenue, units, average
                                      prices and products without sales

  `06_seller_analysis.sql`            Seller counts, top sellers, revenue
                                      by state and sellers without orders

  `07_review_analysis.sql`            Review counts, score distribution,
                                      review categories, average score
                                      and response time

  `08_business_overview.sql`          Compact overall business metrics
  -----------------------------------------------------------------------

### How a SQL runner works

1.  Connect to `ecommerce_analytics.duckdb`.
2.  Read one `.sql` file.
3.  Split the SQL text at semicolons.
4.  Execute each non-empty query.
5.  Print each result.
6.  Close the connection.

### SQL interpretation cautions

-   `gold_revenue` is at **order-item grain**. Use
    `COUNT(DISTINCT order_id)` for order counts and order-level
    averages.
-   Revenue sums include all order statuses unless filtered. Call it
    gross order-item value, not recognized accounting revenue.
-   The Gold Customers table is grouped by `customer_id`. A true
    repeat-customer metric must aggregate across `customer_unique_id`.
-   Repeated `review_id` values are preserved. The candidate composite
    key is `(review_id, order_id)`.
-   A missing category translation can produce a `NULL` category group.

## 6. PySpark files --- inventory and purpose

### Learning and analysis scripts

  -----------------------------------------------------------------------------------
  File                                Purpose                 Concepts
  ----------------------------------- ----------------------- -----------------------
  `01_spark_read_orders.py`           Reads Silver Orders;    `read.parquet`,
                                      prints count, schema    `count`, `printSchema`,
                                      and sample              `show`

  `02_spark_order_analysis.py`        Selects columns,        `select`, `filter`,
                                      filters delivered       `groupBy`, `agg`
                                      orders and groups       
                                      status                  

  `03_spark_product_analysis.py`      Aggregates order items  Grouping, aggregation
                                      by product              and sorting

  `04_spark_customer_analysis.py`     Joins customers to      Joins and customer IDs
                                      order counts            

  `05_spark_revenue_analysis.py`      Joins items to orders   Joins, date formatting
                                      and calculates monthly  and aggregation
                                      item value              

  `06_spark_seller_analysis.py`       Seller-level order-item Grouping and
                                      metrics                 aggregation

  `07_spark_review_analysis.py`       Review score counts and Grouping and averages
                                      averages                

  `08_spark_order_customer_join.py`   Combines order and      Inner join
                                      customer data           

  `09_spark_category_analysis.py`     Joins items, products   Multiple joins
                                      and translations        

  `10_spark_delivery_analysis.py`     Delivery durations,     Date differences,
                                      delay and state-level   aggregation and
                                      performance             customer join
  -----------------------------------------------------------------------------------

### Spark Gold scripts

  ----------------------------------------------------------------------------------------------------------------
  File                           Output                                                    Purpose
  ------------------------------ --------------------------------------------------------- -----------------------
  `11_spark_gold_orders.py`      `data/gold/spark_gold_orders/gold_orders.parquet`         Spark-built order Gold
                                                                                           dataset

  `12_spark_gold_revenue.py`     `data/gold/spark_gold_revenue/gold_revenue.parquet`       Spark-built revenue
                                                                                           Gold dataset

  `13_spark_gold_customers.py`   `data/gold/spark_gold_customers/gold_customers.parquet`   Spark-built customer
                                                                                           metrics

  `14_spark_gold_products.py`    `data/gold/spark_gold_products/gold_products.parquet`     Spark-built product
                                                                                           metrics

  `15_spark_validate_gold.py`    Reads and checks the four Spark Gold Parquet files        File and row-count
                                                                                           validation
  ----------------------------------------------------------------------------------------------------------------

### Important Spark-on-Windows note

Spark reading and transforming the existing Parquet files worked, but
Spark's Hadoop-backed local writer failed because Windows Hadoop
utilities (`HADOOP_HOME` / `winutils.exe`) were not configured.

To avoid Hadoop installation, the revised Spark Gold scripts use:

``` text
Spark reads Parquet
       |
       v
Spark transforms / joins DataFrames
       |
       v
toPandas()
       |
       v
PyArrow converts to Arrow Table
       |
       v
PyArrow writes Parquet
```

This is suitable for the current dataset sizes if the computer has
enough memory. It is **not** suitable for very large datasets because
`toPandas()` collects all rows into driver memory. A larger production
pipeline should use a properly configured Spark writer or managed cloud
Spark service.

### Spark operations to understand

  Operation                    Meaning
  ---------------------------- ---------------------------------------------
  `spark.read.parquet(path)`   Read Parquet
  `select()`                   Choose columns
  `filter()`                   Keep matching rows
  `withColumn()`               Add or replace a column
  `join()`                     Combine DataFrames using a key
  `groupBy()`                  Group records
  `agg()`                      Calculate summary metrics
  `orderBy()`                  Sort rows
  `count()`                    Count rows
  `show()`                     Display sample rows
  `printSchema()`              Display column types
  `toPandas()`                 Collect Spark rows into local Pandas memory

## 7. Data-quality findings

Recorded row counts:

  Dataset            Rows
  ------------- ---------
  Customers        99,441
  Orders           99,441
  Order Items     112,650
  Payments        103,886
  Reviews          99,224
  Products         32,951
  Sellers           3,095

Other recorded findings: - The ID checks performed found no missing key
values. - Referential-integrity orphan counts checked were zero. -
Duplicate-key checks were zero for tested keys except `review_id`. - The
initial duplicate review-ID check reported 814 repeated occurrences. -
Further investigation found 1,603 records with duplicate review IDs, 789
distinct duplicate review IDs, and no duplicate `(review_id, order_id)`
pairs. - Do not remove review rows using `review_id` alone. -
Geolocation has repeated ZIP-prefix values; do not blindly
deduplicate. - Category translation is a mapping table; preserve its
mapping semantics.

## 8. Business logic and caveats

### Delivery

-   `delivery_days` = customer delivery date minus purchase date.
-   `delivery_delay_days` = actual delivery date minus estimated
    delivery date.
-   Positive delay means late; zero or negative means on time or early.
-   Undelivered orders have null actual delivery dates, so delivery-day
    values are null.
-   The Gold Orders logic labels missing delivery dates `not_delivered`.

### Revenue

-   `price` is item price; `freight_value` is item freight.
-   `price + freight_value` is combined item value including freight.
-   The project includes all order statuses unless a query filters them.
-   Do not call this recognized accounting revenue.

### Customers

-   `customer_id` is an order-associated customer record.
-   `customer_unique_id` helps identify the same real customer across
    orders.
-   Grouping by `customer_id` gives record-level metrics.
-   Repeat-customer metrics must group across `customer_unique_id`.

### Products and sellers

-   Units sold should count order-item rows, not sum `order_item_id`.
-   Products without sales should remain in the product dimension with
    zero sales metrics.
-   Seller metrics can include sellers with no sales when the seller
    dimension is left-joined to the sales aggregate.

### Reviews

-   Preserve records using the observed `(review_id, order_id)`
    relationship.
-   A repeated `review_id` alone does not prove duplicate review
    records.

## 9. How to run the project

Open the VS Code PowerShell terminal. Activate the existing environment
if needed:

``` powershell
.\ecom_venv\Scripts\Activate.ps1
```

Move to the project root:

``` powershell
cd "C:\Users\Ashish yadav\OneDrive\Desktop\Ecommerce_Data_Engineering_Project"
```

### Recommended logical execution order

**A. Explore and quality-check raw data**

``` powershell
python python\01_data_exploration.py
python python\02_generate_dataset_report.py
python python\03_data_quality_check.py
python python\04_investigate_duplicate_reviews.py
```

**B. Build Silver (then validate)**

``` powershell
python python\05_silver_customers.py
python python\06_silver_orders.py
python python\07_silver_order_items.py
python python\08_silver_payments.py
python python\09_silver_reviews.py
python python\10_silver_products.py
python python\11_silver_sellers.py
python python\12_silver_geolocation.py
python python\13_silver_category_translation.py
python python\14_validate_silver_layer.py
```

**C. Build original Python Gold (then validate)**

``` powershell
python python\15_gold_orders.py
python python\16_gold_revenue.py
python python\17_gold_customers.py
python python\18_gold_products.py
python python\19_gold_sellers.py
python python\20_gold_reviews.py
python python\21_validate_gold_layer.py
```

**D. Set up DuckDB and run SQL analysis**

``` powershell
python python\22_run_sql_analytics.py
python python\24_execute_sql_file.py
python python\25_run_order_analysis.py
python python\26_run_revenue_analysis.py
python python\27_run_customer_analysis.py
python python\28_run_product_analysis.py
python python\29_run_seller_analysis.py
python python\30_run_review_analysis.py
python python\31_run_business_overview.py
```

**E. Practice PySpark**

Run `pyspark\01_spark_read_orders.py` through
`pyspark\10_spark_delivery_analysis.py` as learning exercises, then run
the four Spark Gold builders and validator:

``` powershell
python pyspark\11_spark_gold_orders.py
python pyspark\12_spark_gold_revenue.py
python pyspark\13_spark_gold_customers.py
python pyspark\14_spark_gold_products.py
python pyspark\15_spark_validate_gold.py
```

Do not rerun overwrite scripts casually. Confirm paths and inputs first.
The Spark Gold scripts write into separate `spark_gold_*` folders.

## 10. Current status and checks to complete

The walkthrough recorded the following as completed: - Nine raw CSVs
downloaded and placed in `data/raw/`. - Exploration and data-quality
scripts run. - Nine Silver Parquet datasets created; Silver validation
script run. - Six original Python Gold datasets created; Gold validation
script run. - DuckDB database and views created. - Eight SQL files and
corresponding runners created and run. - PySpark installed; Java 17
verified. - Spark learning exercises completed through the delivery
exercise, although the first delivery script had an error. - Spark Gold
Revenue, Customers and Products scripts reported completed.

**Verify before AWS:**

1.  `pyspark/10_spark_delivery_analysis.py` originally failed because it
    grouped by `customer_state` without joining the Silver Customers
    dataset. A corrected full version was provided. Re-run it to verify
    the correction.
2.  `pyspark/11_spark_gold_orders.py` initially failed at Spark's
    Hadoop-backed Parquet write. A revised PyArrow-based version was
    provided. Verify that the revised file successfully created
    `spark_gold_orders/gold_orders.parquet`.
3.  Run `pyspark/15_spark_validate_gold.py` after all four Spark Gold
    files exist. Expected counts:
    -   Spark Gold Orders: 99,441
    -   Spark Gold Revenue: 112,650
    -   Spark Gold Customers: 99,441
    -   Spark Gold Products: 32,951
4.  Check that Spark product `units_sold` is calculated by counting
    order-item rows, not by summing `order_item_id`.
5.  Remember that customer repeat analysis must use
    `customer_unique_id`, not only `customer_id`.

A user's confirmation that a task is done records progress, but does not
by itself establish the exact validation output. Re-run the checks if
you need to confirm the files and row counts.

## 11. AWS stage --- planned, not yet configured

Planned architecture:

``` text
Local Gold Parquet datasets
          |
          v
       Amazon S3
     Cloud storage
          |
          v
       AWS Glue
   Catalog / metadata
          |
          v
     Amazon Athena
       SQL queries
```

  Step   Service                            Purpose
  ------ ---------------------------------- ---------------------------------------
  1      AWS account and billing controls   Prepare account safely
  2      Amazon S3                          Create a project bucket
  3      Amazon S3                          Upload selected Gold Parquet datasets
  4      AWS Glue Data Catalog              Create a database/catalog
  5      AWS Glue Crawler                   Discover schemas and register tables
  6      Amazon Athena                      Query S3 Parquet data using SQL
  7      AWS validation                     Verify tables, queries and storage

**Cost and security:** Check current pricing and Free Tier eligibility;
do not assume all services are free. Set a budget alert. Avoid
unnecessary EC2 instances. Never share passwords, access keys, secret
keys or payment details. Remove resources when finished and check for
ongoing storage/query charges.

## 12. Interview explanation

### Short project explanation

"I built an end-to-end e-commerce data engineering pipeline using the
Brazilian Olist dataset. I explored and validated nine raw CSV datasets,
cleaned them into Silver Parquet datasets, and created Gold analytical
datasets using Python. I used DuckDB and SQL for business analysis and
PySpark for DataFrame transformations, joins, aggregations and a
separate Spark Gold layer. The planned next stage is to extend the
pipeline to AWS S3, Glue and Athena."

### Concepts to explain

-   **ETL:** Extract, Transform, Load.
-   **Parquet:** Columnar storage format useful for analytical
    workloads.
-   **Silver:** Cleaned and standardized data.
-   **Gold:** Business-ready analytical data.
-   **DuckDB:** Local analytical SQL database that can query Parquet.
-   **PySpark:** Python API for Spark distributed data processing.
-   **Join:** Combines datasets using a related key.
-   **AWS Glue:** Catalogs data and supports ETL workflows.
-   **Athena:** Runs SQL queries over data in S3.

### Common interview questions

**Why use `customer_unique_id`?** It identifies the same real customer
across multiple order-associated customer records.

**Why preserve repeated review IDs?** The observed
`(review_id, order_id)` pair was unique in the checks; `review_id` alone
was not a safe deduplication key.

**What does the Gold Revenue table represent?** Gross order-item value
including freight at order-item grain, not automatically recognized
accounting revenue.

**Why use PySpark?** To learn and perform DataFrame transformations,
joins and aggregations that can scale to distributed processing.

**Why use Parquet?** It is columnar and supports efficient analytical
reads and compression.

**What is the role of Glue and Athena?** Glue catalogs metadata; Athena
queries data stored in S3 using SQL.

## 13. One-line memory aid

Remember this order:

**RAW → EXPLORE → QUALITY → SILVER → GOLD → SQL → SPARK → AWS**

-   RAW: What did we receive?
-   EXPLORE: What does it look like?
-   QUALITY: Can we trust it?
-   SILVER: Can we clean it?
-   GOLD: Can we prepare it for business use?
-   SQL: What business questions can we answer?
-   SPARK: Can we transform it with Spark?
-   AWS: Can we store, catalog and query it in the cloud?

You do not need to memorize every filename or every line of code. Use
this guide as the project map and learn to explain why each stage exists
and how data moves through it.
