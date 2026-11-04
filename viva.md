# E-Commerce Data Engineering Pipeline — Technical Viva & Interview Preparation

This document contains technical interview and viva questions with answers for the E-Commerce Data Engineering Pipeline built using the Brazilian E-Commerce Public Dataset by Olist.

**How to use this file:** Read the project overview first, then study each topic section. Answers are written in a first-person project-explanation style where useful. Be prepared to open the actual script, SQL query, Parquet file, or AWS table when explaining an implementation.

---

# 1. Project Overview and Architecture

### Q1. What is the objective of this project?

**Answer:** The objective is to build an end-to-end data engineering pipeline using the Brazilian Olist e-commerce dataset. I ingest nine source CSV files, explore and validate the data, transform it into Silver and Gold Parquet datasets, perform analytics using DuckDB and SQL, demonstrate processing with PySpark, and build a Streamlit application for dashboarding and conversational assistance. The cloud stage uses AWS storage and query services where configured.

### Q2. What business problem does the project address?

**Answer:** E-commerce information is distributed across multiple related datasets, such as customers, orders, products, payments, sellers and reviews. The pipeline organizes these files, checks data quality, combines related information and produces analytical datasets that can support questions about orders, revenue, customers, products, sellers, delivery and reviews.

### Q3. Which dataset did you use?

**Answer:** I used the Brazilian E-Commerce Public Dataset by Olist, available on Kaggle. It contains anonymized Brazilian e-commerce activity, mainly from 2016 to 2018, across nine CSV files.

Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

### Q4. What are the main technologies used?

**Answer:**

- Python and Pandas for exploration, validation and transformations.
- PyArrow for Parquet reading/writing and metadata work.
- Parquet as the processed analytical storage format.
- DuckDB as the local analytical SQL database.
- SQL for business analysis.
- PySpark for Spark DataFrame processing.
- Amazon S3 for cloud object storage.
- AWS Glue Data Catalog for table metadata.
- Amazon Athena for SQL queries over S3 data.
- Streamlit for the web dashboard.
- Ollama API with the OpenAI Python client for the simple conversational assistant.

### Q5. Explain the complete project architecture.

**Answer:** The nine original CSV files are stored in the Raw layer. Python scripts explore and validate them. The data is cleaned and standardized into nine Silver Parquet datasets. The Silver datasets are combined and aggregated into six Python Gold datasets. DuckDB and SQL query the Python Gold datasets, while PySpark provides a separate Spark analysis and Spark Gold implementation. The Streamlit app presents local analytical results and a simple AI assistant. The cloud architecture stores selected Gold Parquet files in S3, catalogs them in Glue and queries them through Athena.

### Q6. What is the difference between ETL and ELT?

**Answer:** ETL means Extract, Transform, Load: data is transformed before it is loaded into the target. ELT means Extract, Load, Transform: raw data is first loaded into the target platform and transformed there. This project primarily follows an ETL-style local workflow because Python transforms the raw CSV data into Silver and Gold Parquet outputs before the Gold files are uploaded to cloud storage.

### Q7. Is this a batch or streaming pipeline?

**Answer:** It is a batch pipeline. The source is a fixed collection of CSV files, and scripts process those files when executed. It does not continuously ingest events or process real-time streams.

### Q8. Is this a real-time project?

**Answer:** No. It uses historical public data and batch processing. The dashboard displays analytics based on the locally generated datasets, not a live feed from an e-commerce platform.

### Q9. What is the difference between a data engineering pipeline and a dashboard?

**Answer:** The pipeline ingests, validates, transforms, stores and prepares data. The dashboard is a presentation layer that reads prepared data and displays metrics and visualizations. The dashboard does not replace the data engineering transformations.

### Q10. What is the project execution order?

**Answer:** The logical order is:

1. Place source CSV files in `data/raw/`.
2. Explore the data.
3. Run data-quality checks.
4. Build and validate Silver datasets.
5. Build and validate Python Gold datasets.
6. Set up DuckDB views and run SQL analytics.
7. Run PySpark analysis and Spark Gold scripts.
8. Configure and run the Streamlit app.
9. Upload selected Gold datasets to S3 and query them with Athena when using the AWS stage.

---

# 2. Source Dataset and Data Modeling

### Q11. What are the nine source CSV files?

**Answer:**

1. `olist_customers_dataset.csv`
2. `olist_geolocation_dataset.csv`
3. `olist_order_items_dataset.csv`
4. `olist_order_payments_dataset.csv`
5. `olist_order_reviews_dataset.csv`
6. `olist_orders_dataset.csv`
7. `olist_products_dataset.csv`
8. `olist_sellers_dataset.csv`
9. `product_category_name_translation.csv`

### Q12. What information is stored in the Customers dataset?

**Answer:** It contains customer record identifiers and customer location information, including ZIP-code prefix, city and state. `customer_id` links the customer record to orders, while `customer_unique_id` helps identify the same customer across multiple records.

### Q13. What information is stored in the Orders dataset?

**Answer:** It contains order identifiers, the associated customer record, order status and order lifecycle timestamps such as purchase, approval, carrier handoff, delivery and estimated delivery dates.

### Q14. What information is stored in Order Items?

**Answer:** It contains item-level details for orders, including order ID, item sequence, product ID, seller ID, price and freight value. One order can contain multiple item rows.

### Q15. What information is stored in Payments?

**Answer:** It contains payment information associated with an order, such as payment type, installment count and payment value. An order can have multiple payment records.

### Q16. What information is stored in Reviews?

**Answer:** It contains review identifiers, order identifiers, review scores, comment text and review-related timestamps.

### Q17. What information is stored in Products?

**Answer:** It contains product identifiers and product attributes such as category, name length, description length, photos quantity, weight and dimensions.

### Q18. What information is stored in Sellers?

**Answer:** It contains seller identifiers and seller location information, including ZIP-code prefix, city and state.

### Q19. What is the purpose of the Geolocation dataset?

**Answer:** It maps Brazilian ZIP-code prefixes to geographic coordinates and location information. ZIP prefixes can occur more than once, so the records need an explicit aggregation strategy before being treated as one row per prefix.

### Q20. What is the purpose of the category translation dataset?

**Answer:** It maps Portuguese product category names to English category names. It makes category-level reporting easier to understand.

### Q21. Explain the main table relationships.

**Answer:**

| Relationship | Join key |
|---|---|
| Customers to Orders | `customer_id` |
| Orders to Order Items | `order_id` |
| Orders to Payments | `order_id` |
| Orders to Reviews | `order_id` |
| Order Items to Products | `product_id` |
| Order Items to Sellers | `seller_id` |
| Products to Category Translation | `product_category_name` |

### Q22. What is a primary key?

**Answer:** A primary key is a column or combination of columns that uniquely identifies each row in a table. It should be unique and should not be null.

### Q23. What is a foreign key?

**Answer:** A foreign key is a column that references a key in another table. It represents a relationship between datasets. For example, `customer_id` in Orders references a customer record.

### Q24. What is a composite key?

**Answer:** A composite key is a key made from two or more columns. In the review data, `(review_id, order_id)` was treated as the candidate composite key because `review_id` alone is repeated, while the tested pair had no duplicates.

### Q25. What is the difference between `customer_id` and `customer_unique_id`?

**Answer:** `customer_id` identifies the customer record associated with an order. `customer_unique_id` identifies the same real customer across potentially multiple customer records. For repeat-customer analysis across orders, `customer_unique_id` is the more appropriate identifier.

### Q26. Why can one order have multiple rows in Order Items?

**Answer:** An order can contain multiple products or multiple item entries. Therefore, the order ID repeats in the item table. The item-level grain is identified using the order and item sequence, such as `(order_id, order_item_id)`.

### Q27. Why can one order have multiple payment records?

**Answer:** The payment dataset can contain multiple payment entries for one order, for example where payment is split or represented by multiple payment records. Therefore, joining payments directly to order items can multiply rows if the join grain is not handled carefully.

### Q28. What is data grain?

**Answer:** Grain defines what one row represents in a dataset. For example, one row in Gold Orders represents one order, while one row in Gold Revenue represents one order item. Knowing the grain prevents incorrect aggregation and double counting.

---

# 3. Data Exploration and Data Quality

### Q29. Why did you perform data exploration before transformation?

**Answer:** Exploration helps me understand the source structure before writing transformation logic. I inspect row counts, column names, data types, missing values and sample records. This helps identify data issues and understand how datasets can be joined.

### Q30. Which script performs initial exploration?

**Answer:** `python/01_data_exploration.py`. It inspects all nine CSV files and reports their row counts, columns, data types, missing values and sample rows.

### Q31. Which script generates the dataset summary report?

**Answer:** `python/02_generate_dataset_report.py`. It generates `reports/dataset_summary.txt`.

### Q32. Which script performs data-quality checks?

**Answer:** `python/03_data_quality_check.py`. It checks missing IDs, duplicate keys and referential integrity, and creates `reports/data_quality_report.csv`.

### Q33. What is a missing value?

**Answer:** A missing value is a field that has no recorded value. In Pandas it is commonly represented by `NaN`, `None` or `NaT`, depending on the data type. Missing values need to be understood before deciding whether to retain, replace or remove them.

### Q34. What is a duplicate record?

**Answer:** A duplicate record is a repeated row or repeated business key. A duplicate key does not always mean the complete row is duplicated. The correct uniqueness rule depends on the grain and business meaning of the dataset.

### Q35. What is referential integrity?

**Answer:** Referential integrity means that foreign-key values in a child dataset correspond to valid key values in the parent dataset. For example, every `customer_id` in Orders should match a customer record.

### Q36. What is an orphan record?

**Answer:** An orphan record is a record whose foreign-key value does not match a corresponding parent key. It can indicate missing parent data or an incorrect relationship.

### Q37. What were the recorded row counts for the main source datasets?

**Answer:**

| Dataset | Rows recorded |
|---|---:|
| Customers | 99,441 |
| Orders | 99,441 |
| Order Items | 112,650 |
| Payments | 103,886 |
| Reviews | 99,224 |
| Products | 32,951 |
| Sellers | 3,095 |

The geolocation and category translation row counts should be read from the local exploration report rather than assumed here.

### Q38. What were the key data-quality findings?

**Answer:** The ID checks performed found no missing key values. The tested referential-integrity orphan counts were zero. Duplicate-key checks were zero for the tested keys except `review_id`. The review investigation found repeated review IDs, while no duplicate `(review_id, order_id)` pairs were found in the check.

### Q39. Why did you investigate duplicate review IDs separately?

**Answer:** The review ID was not unique in the source. Deleting rows based only on `review_id` could remove valid reviews associated with different orders. I investigated the relationship between review ID and order ID and preserved the records.

### Q40. What were the duplicate review findings?

**Answer:** The investigation recorded 99,224 review rows, 1,603 records with duplicate review IDs, 789 distinct duplicate review IDs and zero duplicate `(review_id, order_id)` pairs in the check. The important conclusion is not to deduplicate using `review_id` alone.

### Q41. Why should geolocation rows not be blindly deduplicated?

**Answer:** Multiple records can share a ZIP-code prefix but contain different coordinate observations. Removing duplicates arbitrarily can discard geographic information. A defined aggregation rule, such as calculating representative coordinates per prefix, is needed if one row per prefix is required.

### Q42. What is the difference between data validation and data cleaning?

**Answer:** Data validation checks whether data satisfies expected rules, such as non-null keys, uniqueness and valid relationships. Data cleaning applies changes to address issues, such as standardizing data types, handling missing values or correcting formats.

### Q43. Why should original source files remain unchanged?

**Answer:** Keeping the source files unchanged preserves lineage and reproducibility. If transformation logic changes, I can rebuild Silver and Gold from the same original inputs and compare results.

---

# 4. Medallion Architecture: Raw, Silver and Gold

### Q44. What is Medallion Architecture?

**Answer:** Medallion Architecture organizes data into layers, commonly Bronze or Raw, Silver and Gold. Each layer improves the structure and usability of the data. Raw preserves source data, Silver contains cleaned and standardized data, and Gold contains business-oriented datasets.

### Q45. What is the Raw layer in this project?

**Answer:** The Raw layer is `data/raw/`. It stores the nine original Olist CSV files without modifying them.

### Q46. What is the Silver layer?

**Answer:** The Silver layer contains cleaned and standardized versions of the source datasets, stored as Parquet files under `data/processed/silver/`. It provides consistent data for downstream joins and aggregations.

### Q47. What is the Gold layer?

**Answer:** The Gold layer contains business-ready datasets designed for analytics. The project creates six Python Gold datasets and four separate Spark Gold outputs.

### Q48. Why do we need separate layers?

**Answer:** Separate layers make the pipeline easier to understand, validate and maintain. Raw data provides an unchanged source, Silver provides standardized reusable datasets, and Gold provides data shaped for business analysis.

### Q49. Why is Silver not the same as Gold?

**Answer:** Silver focuses on cleaning and standardizing individual source datasets. Gold combines or aggregates data into analytical structures with business metrics and a defined grain.

### Q50. Why store the processed datasets as Parquet?

**Answer:** Parquet is a columnar storage format designed for analytical workloads. It supports efficient reading of selected columns, compression and typed data storage. It is generally more suitable for analytical processing than repeatedly reading large CSV files.

---

# 5. Python and Pandas

### Q51. What is Pandas?

**Answer:** Pandas is a Python library for working with structured data. It provides Series and DataFrame objects and supports reading CSV files, cleaning data, joining datasets, grouping records and calculating metrics.

### Q52. What is a DataFrame?

**Answer:** A DataFrame is a two-dimensional tabular data structure with rows and columns. In this project, CSV and Parquet datasets are read into DataFrames for exploration and transformation.

### Q53. How do you read a CSV file using Pandas?

**Answer:**

```python
import pandas as pd

df = pd.read_csv("data/raw/olist_orders_dataset.csv")
print(df.head())
```

`read_csv()` loads the CSV into a DataFrame, and `head()` displays the first five rows by default.

### Q54. How do you inspect a DataFrame?

**Answer:**

```python
df.head()
df.shape
df.columns
df.dtypes
df.info()
df.isnull().sum()
df.describe()
```

These methods show sample records, dimensions, column names, data types, non-null counts, missing values and descriptive statistics.

### Q55. What does `df.shape` return?

**Answer:** It returns a tuple containing the number of rows and columns, in that order.

### Q56. What does `df.info()` show?

**Answer:** It shows the DataFrame's columns, non-null counts, data types and memory usage.

### Q57. What does `isnull().sum()` do?

**Answer:** `isnull()` marks missing values as true, and `sum()` counts the true values column by column.

### Q58. What is the purpose of `astype()`?

**Answer:** `astype()` converts a Series or DataFrame column to a specified data type when the conversion is valid.

### Q59. What is the purpose of `to_datetime()`?

**Answer:** `pd.to_datetime()` converts values into Pandas datetime values so date arithmetic, filtering and time-based grouping can be performed.

### Q60. What is the purpose of `merge()`?

**Answer:** `merge()` joins two DataFrames using one or more matching columns. It supports join types such as inner, left, right and outer.

### Q61. What is the difference between `groupby()` and `merge()`?

**Answer:** `groupby()` groups rows by one or more columns so that aggregations can be calculated. `merge()` combines columns from related DataFrames using matching keys.

### Q62. What is the difference between `count()` and `sum()`?

**Answer:** `count()` counts non-null values or rows depending on how it is used. `sum()` adds numeric values. For units sold in an order-item table, counting item rows is usually correct; summing `order_item_id` would add sequence numbers rather than count units.

### Q63. What is a left join and why is it useful?

**Answer:** A left join keeps every row from the left dataset and adds matching information from the right dataset. It is useful when all dimension records must remain in the result, including products or sellers with no sales.

### Q64. Why should you validate row counts after joins?

**Answer:** Joins can unintentionally multiply or remove rows. Comparing row counts, key uniqueness and expected grain helps detect incorrect join conditions or one-to-many relationships.

---

# 6. Silver Layer Transformations

### Q65. How many Silver datasets are created?

**Answer:** Nine Silver Parquet datasets are created, one for each source CSV dataset.

### Q66. Where are Silver files stored?

**Answer:** Under `data/processed/silver/`, with a separate folder for each dataset.

### Q67. Which script creates Silver Customers?

**Answer:** `python/05_silver_customers.py`, which writes `data/processed/silver/customers/customers.parquet`.

### Q68. Which script creates Silver Orders?

**Answer:** `python/06_silver_orders.py`, which writes `data/processed/silver/orders/orders.parquet`.

### Q69. Which script creates Silver Order Items?

**Answer:** `python/07_silver_order_items.py`, which writes `data/processed/silver/order_items/order_items.parquet`.

### Q70. Which script creates Silver Payments?

**Answer:** `python/08_silver_payments.py`, which writes `data/processed/silver/payments/payments.parquet`.

### Q71. Which script creates Silver Reviews?

**Answer:** `python/09_silver_reviews.py`, which writes `data/processed/silver/reviews/reviews.parquet`.

### Q72. Which script creates Silver Products?

**Answer:** `python/10_silver_products.py`, which writes `data/processed/silver/products/products.parquet`.

### Q73. Which script creates Silver Sellers?

**Answer:** `python/11_silver_sellers.py`, which writes `data/processed/silver/sellers/sellers.parquet`.

### Q74. Which script creates Silver Geolocation?

**Answer:** `python/12_silver_geolocation.py`, which writes `data/processed/silver/geolocation/geolocation.parquet`.

### Q75. Which script creates Silver Category Translation?

**Answer:** `python/13_silver_category_translation.py`, which writes `data/processed/silver/category_translation/category_translation.parquet`.

### Q76. How do you validate Silver outputs?

**Answer:** Run `python/14_validate_silver_layer.py` after all nine Silver transformation scripts have completed. It validates the generated Silver datasets.

---

# 7. Python Gold Layer and Business Logic

### Q77. How many Python Gold datasets are created?

**Answer:** Six: Gold Orders, Gold Revenue, Gold Customers, Gold Products, Gold Sellers and Gold Reviews.

### Q78. What does Gold Orders contain?

**Answer:** Gold Orders combines order and customer information and calculates delivery-related metrics such as delivery days, delivery delay and delivery status. Its grain is one row per order, keyed by `order_id`.

### Q79. What does Gold Revenue contain?

**Answer:** Gold Revenue combines order items with order, product and category information. It contains item-level price and freight measures and category information. Its grain is one row per `(order_id, order_item_id)`.

### Q80. What does Gold Customers contain?

**Answer:** Gold Customers aggregates order and order-item measures at the `customer_id` record level and joins customer attributes. It contains one row per `customer_id`. It should not be mistaken for a true unique-person repeat-customer table.

### Q81. What does Gold Products contain?

**Answer:** Gold Products contains product attributes and sales metrics. Products without sales are retained so the product dataset does not lose unsold products.

### Q82. What does Gold Sellers contain?

**Answer:** Gold Sellers contains seller-level sales metrics derived from order items and orders, with one row per seller.

### Q83. What does Gold Reviews contain?

**Answer:** Gold Reviews enriches review records with order information and includes review-related fields such as review category and response duration. It preserves the review records using the observed review/order relationship.

### Q84. What are the expected row counts of the six Python Gold datasets?

**Answer:**

| Gold dataset | Expected rows |
|---|---:|
| Gold Orders | 99,441 |
| Gold Revenue | 112,650 |
| Gold Customers | 99,441 |
| Gold Products | 32,951 |
| Gold Sellers | 3,095 |
| Gold Reviews | 99,224 |

These are reference counts from the dataset used during development.

### Q85. How do you validate Gold?

**Answer:** Run `python/21_validate_gold_layer.py` after the six Gold transformations. The validation checks the expected keys and output datasets.

### Q86. How is delivery duration calculated?

**Answer:** `delivery_days` is calculated as the customer delivery timestamp minus the purchase timestamp. The result is expressed in days. If the actual delivery timestamp is missing, the duration remains null.

### Q87. How is delivery delay calculated?

**Answer:** `delivery_delay_days` is calculated as the actual delivery timestamp minus the estimated delivery timestamp. A positive value means delivery was later than estimated; zero or a negative value means delivery was on time or early.

### Q88. How are undelivered orders handled?

**Answer:** If the actual delivery date is missing, delivery duration and delay cannot be calculated. The Gold Orders logic labels missing delivery dates as `not_delivered`.

### Q89. How is item value including freight calculated?

**Answer:** The item price and freight value are combined. Conceptually:

```text
total item value = price + freight_value
```

The Gold Revenue dataset also supports separate item and freight totals.

### Q90. Is Gold Revenue the same as accounting revenue?

**Answer:** No. It is a gross order-item value measure based on item price and freight. The project includes all order statuses unless a query filters them. It should not be described as recognized accounting revenue.

### Q91. Why use `COUNT(DISTINCT order_id)` when counting orders from Gold Revenue?

**Answer:** Gold Revenue has one row per order item, so an order with multiple items appears multiple times. Counting rows would count items, not orders. `COUNT(DISTINCT order_id)` counts each order once.

### Q92. How should true repeat customers be calculated?

**Answer:** Aggregate orders across `customer_unique_id`, count distinct orders for each unique customer and identify customers with more than one order. Grouping only by `customer_id` measures customer records, not necessarily the same person across records.

### Q93. Why retain products with no sales?

**Answer:** Keeping unsold products allows the business to analyze the complete product catalog, not only products that have appeared in order items. A left join from the product dimension to sales aggregates can retain products with zero sales.

### Q94. How should units sold be calculated from order items?

**Answer:** Count the order-item rows for each product, such as `COUNT(*)` after grouping by product. Do not sum `order_item_id`, because it is an item sequence identifier rather than a quantity measure.

---

# 8. DuckDB

### Q95. What is DuckDB?

**Answer:** DuckDB is an analytical database designed for efficient local analytical queries. It can query data files such as Parquet directly and supports SQL without requiring a separate database server for this local workflow.

### Q96. Why did you use DuckDB in this project?

**Answer:** I used DuckDB to create a local analytical database and SQL views over the Gold Parquet files. It allows the project to run business analysis locally without setting up a separate database server.

### Q97. What is the DuckDB database file called?

**Answer:** `ecommerce_analytics.duckdb`, located in the project root.

### Q98. What does `read_parquet()` do in DuckDB?

**Answer:** `read_parquet()` reads Parquet data from a file path and makes it available to a query. In this project, the SQL setup creates views over the Gold Parquet files.

### Q99. What is a SQL view?

**Answer:** A view is a named SQL query that can be queried like a table. The project's Gold views provide convenient names for the Parquet datasets without requiring a separate data copy.

### Q100. Which file creates the six Gold views?

**Answer:** `sql/01_database_setup.sql`.

### Q101. What does `22_run_sql_analytics.py` do?

**Answer:** It connects to `ecommerce_analytics.duckdb` and registers views over the Gold Parquet datasets.

### Q102. What does `24_execute_sql_file.py` do?

**Answer:** It executes the SQL setup file to create or refresh the views and prints database table/view information.

### Q103. Why use DuckDB instead of a traditional database server?

**Answer:** DuckDB is lightweight for local analytics, can query Parquet directly and does not require managing a separate database server. It fits the local analysis requirements of this project.

### Q104. Is DuckDB the same as a data lake?

**Answer:** No. A data lake is a storage approach for files and datasets, often on object storage. DuckDB is an analytical database engine that can query data stored in files or tables.

---

# 9. SQL Analytics

### Q105. Which SQL file analyzes orders?

**Answer:** `sql/02_order_analysis.sql`. It analyzes order counts, order status, delivery status, delivery duration, delay and state-level order information.

### Q106. Which SQL file analyzes revenue?

**Answer:** `sql/03_revenue_analysis.sql`. It analyzes item value, freight, combined item value, monthly revenue, category revenue and average order value.

### Q107. Which SQL file analyzes customers?

**Answer:** `sql/04_customer_analysis.sql`. It analyzes customer records, spending, state summaries and customer order patterns. The repeat-customer interpretation must account for the distinction between `customer_id` and `customer_unique_id`.

### Q108. Which SQL file analyzes products?

**Answer:** `sql/05_product_analysis.sql`. It analyzes product counts, top products, category revenue, units, average prices and products without sales.

### Q109. Which SQL file analyzes sellers?

**Answer:** `sql/06_seller_analysis.sql`. It analyzes seller counts, seller performance, revenue by state and sellers without orders.

### Q110. Which SQL file analyzes reviews?

**Answer:** `sql/07_review_analysis.sql`. It analyzes review counts, score distribution, review categories, average scores and response time.

### Q111. Which SQL file provides an overall business summary?

**Answer:** `sql/08_business_overview.sql`.

### Q112. What is an aggregate function?

**Answer:** An aggregate function calculates a summary from multiple rows. Examples include `COUNT()`, `SUM()`, `AVG()`, `MIN()` and `MAX()`.

### Q113. What is the difference between `WHERE` and `HAVING`?

**Answer:** `WHERE` filters rows before grouping and aggregation. `HAVING` filters groups after `GROUP BY` and aggregate calculations.

### Q114. What is `GROUP BY` used for?

**Answer:** `GROUP BY` groups rows that share the same value in one or more columns so aggregate calculations can be performed for each group.

### Q115. What is `ORDER BY` used for?

**Answer:** `ORDER BY` sorts query results by one or more columns, ascending by default or descending with `DESC`.

### Q116. What is the difference between `COUNT(*)` and `COUNT(column)`?

**Answer:** `COUNT(*)` counts rows. `COUNT(column)` counts only rows where that column is not null.

### Q117. What is average order value (AOV)?

**Answer:** AOV is the average value per order. Conceptually:

```text
AOV = total order value / number of distinct orders
```

The numerator and denominator must use compatible filters and the correct order-level grain. If using an item-level table, aggregate item values to orders or divide by the distinct order count rather than the item-row count.

### Q118. Why can a join create duplicate-looking rows?

**Answer:** A join can produce multiple output rows when the join key is not unique on one or both sides. For example, one order can have multiple order items and multiple payment records. The join cardinality must be understood before aggregation.

### Q119. What is a one-to-many relationship?

**Answer:** It is a relationship where one row in a parent dataset can match multiple rows in a child dataset. One order can match multiple order-item records.

### Q120. What is an inner join?

**Answer:** An inner join returns only rows with matching keys in both datasets.

### Q121. What is a left join?

**Answer:** A left join returns all rows from the left dataset and matching rows from the right dataset. Unmatched right-side columns are null.

### Q122. Why is SQL analysis separated into multiple files?

**Answer:** Separate SQL files organize the queries by business domain—orders, revenue, customers, products, sellers, reviews and overview. This makes the analysis easier to navigate and maintain.

---

# 10. PySpark

### Q123. What is Apache Spark?

**Answer:** Apache Spark is a distributed data processing engine designed for large-scale data processing and analytics. It can process data across multiple machines and provides APIs for SQL, DataFrames, streaming and machine learning.

### Q124. What is PySpark?

**Answer:** PySpark is the Python API for Apache Spark. It allows Python code to use Spark DataFrames and Spark processing operations.

### Q125. Why did you include PySpark in this project?

**Answer:** PySpark demonstrates how the same business data can be read, joined, filtered and aggregated using Spark DataFrames. It provides experience with distributed-processing concepts in addition to Pandas and DuckDB.

### Q126. What is a Spark DataFrame?

**Answer:** A Spark DataFrame is a distributed collection of data organized into named columns. It has a schema and supports transformations such as selecting columns, filtering, joining and grouping.

### Q127. What is a SparkSession?

**Answer:** A SparkSession is the entry point for using Spark functionality in a Spark application. It is used to read data and create or operate on DataFrames.

### Q128. How do you read a Parquet file in PySpark?

**Answer:**

```python
df = spark.read.parquet("data/processed/silver/orders/orders.parquet")
```

This reads the Parquet dataset into a Spark DataFrame.

### Q129. What does `printSchema()` do?

**Answer:** It prints the DataFrame schema, including column names and data types.

### Q130. What does `show()` do?

**Answer:** It displays a sample of rows from a Spark DataFrame.

### Q131. What does `select()` do?

**Answer:** It selects specified columns or expressions from a DataFrame.

### Q132. What does `filter()` do?

**Answer:** It returns rows that satisfy a Boolean condition.

### Q133. What does `withColumn()` do?

**Answer:** It adds a new column or replaces an existing column using a Spark expression.

### Q134. What does `join()` do?

**Answer:** It combines two Spark DataFrames using matching columns or a join condition.

### Q135. What does `groupBy()` do?

**Answer:** It groups rows by one or more columns so aggregate functions can be applied.

### Q136. What does `agg()` do?

**Answer:** It applies one or more aggregate expressions, such as count, sum or average, to grouped or ungrouped data.

### Q137. What is the difference between Pandas and PySpark DataFrames?

**Answer:** A Pandas DataFrame is generally processed in local memory on one machine. A Spark DataFrame is designed for distributed processing and can be partitioned across a Spark cluster. The APIs have similar concepts, but their execution models differ.

### Q138. What is lazy evaluation in Spark?

**Answer:** Spark transformations generally build a logical execution plan rather than immediately processing all data. Execution is triggered by an action such as `show()`, `count()` or writing output.

### Q139. What is the difference between a transformation and an action in Spark?

**Answer:** A transformation creates a new DataFrame or execution-plan step, such as `select()`, `filter()` or `join()`. An action triggers execution and returns a result or writes data, such as `count()`, `show()` or a write operation.

### Q140. What is a Spark shuffle?

**Answer:** A shuffle is the redistribution of data across partitions, often required for operations such as joins and group-by aggregations. It can be expensive because it may involve network transfer and disk I/O.

### Q141. What is a partition in Spark?

**Answer:** A partition is a logical division of a distributed dataset. Spark uses partitions to process data in parallel.

### Q142. What is the role of Java in PySpark?

**Answer:** Apache Spark runs on the JVM, so a compatible Java runtime is required. The development environment for this project used OpenJDK 17.

### Q143. Why did the project avoid installing Hadoop and winutils?

**Answer:** On Windows, Spark's Hadoop-backed local Parquet writer raised a dependency issue involving `HADOOP_HOME` and `winutils.exe`. Rather than adding Hadoop setup complexity, the revised Spark Gold scripts collected the results with `toPandas()` and wrote Parquet using PyArrow.

### Q144. Explain the Spark Gold writing workaround.

**Answer:** Spark reads and transforms the Parquet data using Spark DataFrames. The final DataFrame is converted to Pandas using `toPandas()`, converted to an Arrow table and written to Parquet using PyArrow. This avoids the Hadoop-backed Spark writer in the local Windows environment.

### Q145. What is the limitation of `toPandas()`?

**Answer:** `toPandas()` collects the Spark DataFrame into the driver machine's memory. The full result must fit in local memory. This is acceptable for the current dataset if sufficient memory is available, but it is not appropriate for very large distributed datasets.

### Q146. How should a production Spark pipeline write large Parquet outputs?

**Answer:** A production implementation should use Spark's distributed write capability with a correctly configured environment or a managed Spark platform. It should avoid collecting the full distributed dataset into one machine's Pandas memory.

### Q147. What are the Spark Gold datasets?

**Answer:** The project creates four separate Spark Gold outputs: Spark Gold Orders, Spark Gold Revenue, Spark Gold Customers and Spark Gold Products. They are stored in separate `spark_gold_*` folders and do not replace the six original Python Gold datasets.

### Q148. Why are there ten Gold folders?

**Answer:** There are six original Python Gold datasets and four separate Spark Gold implementations. The Spark outputs are additional implementations and should not be confused with or overwrite the original Python Gold outputs.

---

# 11. AWS: S3, Glue and Athena

### Q149. What is Amazon S3?

**Answer:** Amazon Simple Storage Service (S3) is object storage. It stores objects inside buckets and is commonly used to store data files such as Parquet datasets.

### Q150. What is an S3 bucket?

**Answer:** A bucket is a top-level container for objects in S3. Objects are organized using keys, which can include prefixes that look like folders.

### Q151. Why store Gold Parquet files in S3?

**Answer:** S3 provides durable cloud object storage for the prepared analytical datasets. Storing Gold Parquet files in S3 makes them available to cloud analytics services such as Athena.

### Q152. What is an S3 prefix?

**Answer:** A prefix is the beginning of an object key. It is commonly used to organize objects into folder-like groups, such as `gold_orders/` or `gold_revenue/`.

### Q153. What is AWS Glue?

**Answer:** AWS Glue is a managed data integration service. Its Data Catalog stores metadata about datasets, databases and tables so other analytics services can discover and query the data.

### Q154. What is the Glue Data Catalog?

**Answer:** It is a centralized metadata catalog. It stores information such as database names, table definitions, column names, data types and storage locations.

### Q155. What is a Glue database?

**Answer:** A Glue database is a logical container for table metadata. In this project the database name used during development was `ecommerce_analytics_db`.

### Q156. What is a Glue crawler?

**Answer:** A Glue crawler can inspect data sources, infer schemas and create or update Data Catalog table definitions. The project guide describes crawler creation as planned, while the development walkthrough also recorded that crawler creation was restricted in the account. The actual table-creation method should be described according to the AWS setup currently present.

### Q157. What is Amazon Athena?

**Answer:** Amazon Athena is a serverless interactive query service that uses SQL to query data stored in sources such as Amazon S3. It can query Parquet data using table metadata from the Glue Data Catalog.

### Q158. Does Athena store a separate copy of the S3 data?

**Answer:** Athena queries the data in its storage location, such as S3. The Data Catalog stores metadata about the table; it is not a duplicate copy of all the underlying Parquet records.

### Q159. What is an external table in Athena?

**Answer:** An external table is a table definition that describes data stored outside Athena, commonly in S3. The table specifies the schema, file format and S3 location.

### Q160. Why use Parquet with Athena?

**Answer:** Parquet is columnar, so Athena can read only the columns needed by a query. This can reduce the amount of data scanned compared with reading an equivalent CSV dataset, depending on layout and query.

### Q161. What is an Athena query-results location?

**Answer:** Athena writes query output and metadata to an S3 location configured for the workgroup or query execution. This location is separate from the source data location.

### Q162. Why is S3 Block Public Access important?

**Answer:** It helps prevent accidental public exposure of bucket contents. Project data should remain private unless there is a specific, reviewed requirement to make it public.

### Q163. How does Athena pricing generally work?

**Answer:** Athena query pricing is generally based on the amount of data scanned, subject to the current pricing model and account terms. Columnar formats, compression, partitioning and selecting only needed columns can help reduce scanning. Always check current AWS pricing.

### Q164. Does AWS Free Tier mean every AWS service is free?

**Answer:** No. Free-tier eligibility, credits, limits and service charges vary. Storage, queries and other resources can incur charges. Monitor billing and budgets.

### Q165. What schema mismatch issue can happen with Parquet and Athena?

**Answer:** Athena table column types must be compatible with the physical Parquet schema. If a table declares a column with the wrong type, Athena can return a schema mismatch or conversion error. The correct fix is to inspect the actual Parquet schema and define the Athena column type accordingly.

### Q166. Which type corrections were needed in this project?

**Answer:** The development notes recorded these mappings:

- Gold Orders `delivery_days` and `delivery_delay_days` were `DOUBLE`.
- Gold Customers `customer_zip_code_prefix` was mapped to Athena `STRING`.
- Gold Products `product_name_lenght`, `product_description_lenght` and `product_photos_qty` were `DOUBLE`.

The physical Parquet schema should always be checked before defining or altering a table.

### Q167. What AWS resources should be protected?

**Answer:** S3 buckets, IAM credentials, access keys, secret keys, account passwords and billing information should be protected. Do not commit credentials to Git or expose them in screenshots.

---

# 12. Streamlit Dashboard and AI Business Assistant

### Q168. What is Streamlit?

**Answer:** Streamlit is a Python framework for creating interactive web applications, especially data applications and dashboards, using Python code.

### Q169. Where is the Streamlit application located?

**Answer:** The application file is `app.py` in the project root.

### Q170. How do you run the Streamlit application?

**Answer:** Activate the project virtual environment, open the project root in the terminal and run:

```powershell
python -m streamlit run app.py
```

Streamlit prints a local URL, commonly `http://localhost:8501`.

### Q171. What are the main sections of the application?

**Answer:** The app has a Business Dashboard section and an AI Business Assistant section. The dashboard reads local analytical data through DuckDB, while the assistant generates conversational answers using the configured Ollama API model.

### Q172. Is the AI assistant connected to DuckDB?

**Answer:** No. The assistant in this project is a simple conversational answer generator. It is not configured as a SQL agent, a database-querying chatbot or a retrieval-augmented generation system. It should not be described as reading live dashboard metrics.

### Q173. What is Ollama in this project?

**Answer:** Ollama provides access to the selected language model through the configured API. The application uses an OpenAI-compatible Python client configured with the provider's API key, model name and base URL.

### Q174. Why use environment variables?

**Answer:** Environment variables keep configuration and secrets outside the source code. The `.env` file stores the API key, model name and API base URL for local development.

### Q175. What does `python-dotenv` do?

**Answer:** `python-dotenv` loads variables from a local `.env` file into the process environment so the Python application can access them using environment-variable functions.

### Q176. Why should `.env` not be uploaded to GitHub?

**Answer:** It can contain API keys and other secrets. Uploading it can expose credentials and allow unauthorized use. `.env` should be listed in `.gitignore`, and exposed keys should be rotated.

### Q177. What is the purpose of the OpenAI Python package in this app?

**Answer:** The `openai` Python package provides the client interface used by the application to make chat-completion requests to an OpenAI-compatible API endpoint. The endpoint, API key and model name are supplied through configuration.

### Q178. What is a chat completion?

**Answer:** A chat completion is a generated assistant response based on a sequence of messages, commonly including system instructions, user messages and previous assistant messages.

### Q179. What is a system prompt?

**Answer:** A system prompt provides high-level instructions about the assistant's role, behavior and response constraints. It is separate from the user's individual message.

### Q180. What is Streamlit session state?

**Answer:** Session state stores values across Streamlit reruns for a user's session. It can be used to retain chat history or selected application state while the user interacts with the app.

### Q181. What happens if the API key or model name is incorrect?

**Answer:** The API request can fail with an authentication, model-not-found or configuration error. Check the `.env` variable names, key validity, model identifier and API base URL against the provider's current documentation. Restart the app after changing environment variables.

### Q182. What does `ModuleNotFoundError: No module named 'openai'` mean?

**Answer:** It means the Python environment running the application cannot find the `openai` package. Install it in the same activated virtual environment using:

```powershell
python -m pip install openai
```

### Q183. What does `ModuleNotFoundError: No module named 'dotenv'` mean?

**Answer:** It means `python-dotenv` is not installed in the active environment. Install it using:

```powershell
python -m pip install python-dotenv
```

---

# 13. Python Environment, Dependencies and Git

### Q184. Why use a virtual environment?

**Answer:** A virtual environment isolates the project's Python packages from other projects and the system Python installation. It helps avoid dependency conflicts and makes the project easier to reproduce.

### Q185. What is the name of this project's virtual environment?

**Answer:** `ecom_venv`.

### Q186. How do you activate it in Windows PowerShell?

**Answer:**

```powershell
.\ecom_venv\Scripts\Activate.ps1
```

### Q187. What is `pip`?

**Answer:** `pip` is Python's package installer. It installs and manages packages from package indexes or other supported sources.

### Q188. What is `requirements.txt`?

**Answer:** It is a text file listing Python dependencies for the project. Another environment can install the listed packages using:

```powershell
python -m pip install -r requirements.txt
```

### Q189. How can you generate `requirements.txt`?

**Answer:**

```powershell
python -m pip freeze > requirements.txt
```

This records installed packages in the active environment. For a production project, a curated dependency list with tested version constraints can be preferable to a full environment freeze.

### Q190. What is Git?

**Answer:** Git is a distributed version-control system. It tracks source-code changes and supports commits, branches and collaboration.

### Q191. What is GitHub?

**Answer:** GitHub is a hosting platform for Git repositories. It provides remote repository storage and collaboration features.

### Q192. What is `.gitignore`?

**Answer:** `.gitignore` lists files and directories that Git should normally ignore when identifying untracked files. This project should ignore virtual environments, secrets, local database files, generated datasets, caches and temporary output.

### Q193. Which project files should not be committed?

**Answer:** At minimum, do not commit `.env`, API keys, passwords, private credentials, the `ecom_venv/` virtual environment, large generated datasets unless intentionally required, local DuckDB files and temporary Spark output.

### Q194. Does adding `.env` to `.gitignore` remove it from Git history?

**Answer:** No. `.gitignore` prevents untracked files from being added automatically, but it does not remove a file already tracked or committed. If a secret was committed, remove it from tracking and rotate the exposed credential. Removing it from the latest commit may not remove it from repository history.

### Q195. What does `git status` do?

**Answer:** It shows the current branch state and reports modified, staged, untracked and other relevant repository changes.

### Q196. What do `git add`, `git commit` and `git push` do?

**Answer:**

- `git add` stages selected changes.
- `git commit` saves a snapshot of staged changes in local repository history.
- `git push` sends local commits to a remote repository such as GitHub.

### Q197. Why check `git status` before committing?

**Answer:** It helps verify that only intended source and documentation files are staged and that secrets, virtual environments, local databases and large data files are not included.

---

# 14. File-by-File Project Reference

## Python scripts

| Script | Technical purpose |
|---|---|
| `01_data_exploration.py` | Inspects nine CSV files: rows, columns, types, nulls and samples |
| `02_generate_dataset_report.py` | Creates `reports/dataset_summary.txt` |
| `03_data_quality_check.py` | Checks missing IDs, duplicate keys and referential integrity; creates CSV report |
| `04_investigate_duplicate_reviews.py` | Investigates duplicate review IDs and composite-key behavior |
| `05_silver_customers.py` | Creates Silver Customers Parquet |
| `06_silver_orders.py` | Creates Silver Orders Parquet |
| `07_silver_order_items.py` | Creates Silver Order Items Parquet |
| `08_silver_payments.py` | Creates Silver Payments Parquet |
| `09_silver_reviews.py` | Creates Silver Reviews Parquet |
| `10_silver_products.py` | Creates Silver Products Parquet |
| `11_silver_sellers.py` | Creates Silver Sellers Parquet |
| `12_silver_geolocation.py` | Creates Silver Geolocation Parquet |
| `13_silver_category_translation.py` | Creates Silver Category Translation Parquet |
| `14_validate_silver_layer.py` | Validates Silver outputs |
| `15_gold_orders.py` | Builds one-row-per-order Gold dataset |
| `16_gold_revenue.py` | Builds order-item-level revenue dataset |
| `17_gold_customers.py` | Builds customer-record-level metrics |
| `18_gold_products.py` | Builds product metrics and retains products without sales |
| `19_gold_sellers.py` | Builds seller metrics |
| `20_gold_reviews.py` | Enriches review records with order data |
| `21_validate_gold_layer.py` | Validates six Python Gold outputs |
| `22_run_sql_analytics.py` | Connects DuckDB and registers Gold Parquet views |
| `24_execute_sql_file.py` | Executes SQL setup file |
| `25_run_order_analysis.py` | Runs order SQL analysis |
| `26_run_revenue_analysis.py` | Runs revenue SQL analysis |
| `27_run_customer_analysis.py` | Runs customer SQL analysis |
| `28_run_product_analysis.py` | Runs product SQL analysis |
| `29_run_seller_analysis.py` | Runs seller SQL analysis |
| `30_run_review_analysis.py` | Runs review SQL analysis |
| `31_run_business_overview.py` | Runs business overview SQL |

**Numbering note:** The project history does not document a `23_...` Python file. Do not invent a purpose for a missing number.

## SQL files

| SQL file | Technical purpose |
|---|---|
| `01_database_setup.sql` | Creates six DuckDB views over Python Gold Parquet |
| `02_order_analysis.sql` | Order, status, delivery and state analytics |
| `03_revenue_analysis.sql` | Item value, freight, monthly and category analysis |
| `04_customer_analysis.sql` | Customer counts and spending analysis |
| `05_product_analysis.sql` | Product, category, price and no-sales analysis |
| `06_seller_analysis.sql` | Seller metrics and seller-state analysis |
| `07_review_analysis.sql` | Review score and response-time analysis |
| `08_business_overview.sql` | Consolidated business metrics |

## PySpark scripts

| Script | Technical purpose |
|---|---|
| `01_spark_read_orders.py` | Reads Silver Orders and displays count, schema and sample |
| `02_spark_order_analysis.py` | Filters and groups order data |
| `03_spark_product_analysis.py` | Aggregates order items by product |
| `04_spark_customer_analysis.py` | Joins customers and order counts |
| `05_spark_revenue_analysis.py` | Joins items and orders; calculates monthly item value |
| `06_spark_seller_analysis.py` | Seller-level aggregation |
| `07_spark_review_analysis.py` | Review score counts and averages |
| `08_spark_order_customer_join.py` | Joins order and customer data |
| `09_spark_category_analysis.py` | Joins items, products and category translations |
| `10_spark_delivery_analysis.py` | Delivery duration, delay and state analysis |
| `11_spark_gold_orders.py` | Creates Spark Gold Orders |
| `12_spark_gold_revenue.py` | Creates Spark Gold Revenue |
| `13_spark_gold_customers.py` | Creates Spark Gold Customers |
| `14_spark_gold_products.py` | Creates Spark Gold Products |
| `15_spark_validate_gold.py` | Validates four Spark Gold datasets |

---

# 15. Important Technical Caveats

1. **Revenue interpretation:** Gold Revenue is based on order-item price and freight. It includes all order statuses unless filtered. Describe it as gross order-item value, not recognized accounting revenue.
2. **Customer identity:** Gold Customers is grouped by `customer_id`. True repeat-customer analysis must use `customer_unique_id`.
3. **Review uniqueness:** `review_id` alone is not unique in the source. Preserve records and use `(review_id, order_id)` as the candidate composite key found in the checks.
4. **Geolocation:** ZIP-code prefixes repeat. Do not blindly deduplicate them.
5. **Order-item grain:** Gold Revenue has one row per order item. Use distinct order IDs for order counts.
6. **Spark product units:** Units sold should count order-item rows, not sum `order_item_id`.
7. **Spark memory:** `toPandas()` collects Spark data into driver memory. This workaround is suitable only while the result fits in local memory.
8. **Spark and Windows:** The project avoided installing Hadoop/winutils and used PyArrow for Spark Gold output.
9. **Separate Gold branches:** Six Python Gold outputs and four Spark Gold outputs are separate implementations.
10. **AI assistant scope:** The assistant generates conversational answers; it is not connected to DuckDB and does not generate SQL against project data.
11. **Dataset age:** The Olist data is historical and does not represent live transactions.
12. **Dataset license:** The project guide identified the dataset as CC BY-NC-SA 4.0. Retain attribution and check the current license terms before redistribution or commercial use.
13. **AWS status:** The master guide supplied with the project describes AWS as a planned stage. If the current AWS resources have since been created, update your project status and describe only the resources and queries you have personally verified.
14. **Reproducibility:** Run scripts from the project root so relative paths resolve correctly. Validate outputs after each layer.

---

# 16. Practical Viva Demonstration Sequence

When asked to demonstrate the project, use this technical sequence:

1. Open the project root and explain the folder structure.
2. Show the nine source CSVs in `data/raw/`.
3. Open the exploration and quality scripts and their reports.
4. Show the duplicate review investigation and explain the composite-key decision.
5. Show the nine Silver Parquet outputs and the Silver validation script.
6. Show the six Python Gold datasets and explain the grain of each.
7. Open one Gold transformation script and explain its input, joins, calculations and output.
8. Show the DuckDB database setup and the SQL analysis files.
9. Run one or more SQL analytics scripts and explain the result.
10. Show PySpark reading, joins, aggregations and separate Spark Gold outputs.
11. Explain the Windows Spark writer workaround and its memory limitation.
12. Show S3, Glue and Athena only for resources that are currently configured and verified.
13. Run `app.py` and demonstrate the dashboard.
14. Demonstrate the AI assistant and explain that it is not database-connected.
15. Show `.gitignore` and explain how API keys and generated data are protected.

---

# 17. Quick Revision: One-Line Definitions

| Term | Quick definition |
|---|---|
| Data pipeline | A sequence of steps that moves and transforms data |
| ETL | Extract, Transform, Load |
| Batch processing | Processing a bounded set of data at scheduled or manual intervals |
| Raw layer | Original source data |
| Silver layer | Cleaned and standardized data |
| Gold layer | Business-ready analytical data |
| DataFrame | A tabular data structure with rows and columns |
| Primary key | Unique identifier for a row |
| Foreign key | Field that references a related dataset's key |
| Composite key | Key made from multiple columns |
| Data grain | What one row represents |
| Referential integrity | Valid relationships between related datasets |
| Parquet | Columnar file format for analytics |
| Pandas | Python library for local tabular data analysis |
| PyArrow | Python library for Apache Arrow and Parquet operations |
| DuckDB | Local analytical SQL database engine |
| SQL view | Named query that can be queried like a table |
| PySpark | Python API for Apache Spark |
| SparkSession | Entry point for a Spark application |
| Lazy evaluation | Spark defers execution until an action is called |
| Transformation | Operation that creates a new Spark execution-plan step |
| Action | Operation that triggers Spark execution |
| Shuffle | Redistribution of data across Spark partitions |
| S3 | AWS object storage service |
| Glue Data Catalog | Metadata catalog for datasets and tables |
| Glue crawler | Tool that discovers schemas and catalog tables |
| Athena | Serverless SQL query service for data in S3 |
| Streamlit | Python framework for interactive data apps |
| Environment variable | Configuration value supplied outside source code |
| `.env` | Local file commonly used to store development configuration |
| Git | Distributed version control |
| GitHub | Hosting platform for Git repositories |
| `.gitignore` | Rules for files Git should ignore |

---

**End of technical viva guide.**
