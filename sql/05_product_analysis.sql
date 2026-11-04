
-- ============================================
-- E-COMMERCE PRODUCT ANALYSIS
-- ============================================

-- QUERY 1: Total products
SELECT
    COUNT(*) AS total_products
FROM gold_products;


-- QUERY 2: Top 10 products by revenue
SELECT
    product_id,
    product_category_name_english,
    units_sold,
    ROUND(total_revenue, 2) AS total_revenue
FROM gold_products
ORDER BY total_revenue DESC
LIMIT 10;


-- QUERY 3: Revenue by product category
SELECT
    product_category_name_english,
    ROUND(SUM(total_revenue), 2) AS category_revenue
FROM gold_products
GROUP BY product_category_name_english
ORDER BY category_revenue DESC
LIMIT 10;


-- QUERY 4: Top 10 products by units sold
SELECT
    product_id,
    product_category_name_english,
    units_sold
FROM gold_products
ORDER BY units_sold DESC
LIMIT 10;


-- QUERY 5: Average selling price by category
SELECT
    product_category_name_english,
    ROUND(AVG(average_price), 2) AS average_selling_price
FROM gold_products
WHERE average_price IS NOT NULL
GROUP BY product_category_name_english
ORDER BY average_selling_price DESC
LIMIT 10;


-- QUERY 6: Products without sales
SELECT
    COUNT(*) AS products_without_sales
FROM gold_products
WHERE units_sold = 0;
