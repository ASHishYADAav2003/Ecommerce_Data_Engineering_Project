
-- ============================================
-- E-COMMERCE REVENUE ANALYSIS
-- ============================================

-- QUERY 1: Total product revenue
SELECT
    ROUND(SUM(total_item_revenue), 2) AS total_product_revenue
FROM gold_revenue;


-- QUERY 2: Total freight revenue
SELECT
    ROUND(SUM(total_freight_revenue), 2) AS total_freight_revenue
FROM gold_revenue;


-- QUERY 3: Combined item and freight value
SELECT
    ROUND(SUM(total_order_item_value), 2) AS total_value
FROM gold_revenue;


-- QUERY 4: Monthly revenue
SELECT
    purchase_month,
    ROUND(SUM(total_item_revenue), 2) AS monthly_revenue
FROM gold_revenue
GROUP BY purchase_month
ORDER BY purchase_month;


-- QUERY 5: Top 10 product categories by revenue
SELECT
    product_category_name_english,
    ROUND(SUM(total_item_revenue), 2) AS total_revenue
FROM gold_revenue
GROUP BY product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;


-- QUERY 6: Average order value
SELECT
    ROUND(
        SUM(total_order_item_value) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM gold_revenue;
