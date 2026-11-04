-- 1. Total number of sellers
SELECT
    COUNT(*) AS total_sellers
FROM gold_sellers;


-- 2. Top 10 sellers by revenue
SELECT
    seller_id,
    seller_state,
    ROUND(total_product_revenue, 2) AS total_revenue
FROM gold_sellers
ORDER BY total_product_revenue DESC
LIMIT 10;


-- 3. Top 10 sellers by number of orders
SELECT
    seller_id,
    total_orders
FROM gold_sellers
ORDER BY total_orders DESC
LIMIT 10;


-- 4. Seller revenue by state
SELECT
    seller_state,
    ROUND(SUM(total_product_revenue), 2) AS state_revenue
FROM gold_sellers
GROUP BY seller_state
ORDER BY state_revenue DESC;


-- 5. Average revenue per seller
SELECT
    ROUND(AVG(total_product_revenue), 2) AS average_revenue_per_seller
FROM gold_sellers;


-- 6. Sellers without orders
SELECT
    COUNT(*) AS sellers_without_orders
FROM gold_sellers
WHERE total_orders = 0;