-- 1. Total orders
SELECT COUNT(*) AS total_orders
FROM gold_orders;


-- 2. Total order item value
SELECT
    ROUND(SUM(total_order_item_value), 2) AS total_order_item_value
FROM gold_revenue;


-- 3. Total customers
SELECT COUNT(*) AS total_customers
FROM gold_customers;


-- 4. Total products
SELECT COUNT(*) AS total_products
FROM gold_products;


-- 5. Total sellers
SELECT COUNT(*) AS total_sellers
FROM gold_sellers;


-- 6. Average review score
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM gold_reviews;