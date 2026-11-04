
-- ============================================
-- E-COMMERCE DATABASE SETUP
-- Create views from Gold Parquet datasets
-- ============================================

CREATE OR REPLACE VIEW gold_orders AS
SELECT *
FROM read_parquet('data/gold/gold_orders/gold_orders.parquet');


CREATE OR REPLACE VIEW gold_revenue AS
SELECT *
FROM read_parquet('data/gold/gold_revenue/gold_revenue.parquet');


CREATE OR REPLACE VIEW gold_customers AS
SELECT *
FROM read_parquet('data/gold/gold_customers/gold_customers.parquet');


CREATE OR REPLACE VIEW gold_products AS
SELECT *
FROM read_parquet('data/gold/gold_products/gold_products.parquet');


CREATE OR REPLACE VIEW gold_sellers AS
SELECT *
FROM read_parquet('data/gold/gold_sellers/gold_sellers.parquet');


CREATE OR REPLACE VIEW gold_reviews AS
SELECT *
FROM read_parquet('data/gold/gold_reviews/gold_reviews.parquet');
