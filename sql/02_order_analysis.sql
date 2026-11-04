
-- ============================================
-- E-COMMERCE ORDER ANALYSIS
-- ============================================

-- QUERY 1: Total number of orders
SELECT
    COUNT(*) AS total_orders
FROM gold_orders;


-- QUERY 2: Orders by status
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM gold_orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- QUERY 3: Delivery performance distribution
SELECT
    delivery_status,
    COUNT(*) AS total_orders
FROM gold_orders
GROUP BY delivery_status
ORDER BY total_orders DESC;


-- QUERY 4: Average delivery time in days
SELECT
    ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM gold_orders
WHERE delivery_days IS NOT NULL;


-- QUERY 5: Average delivery delay
SELECT
    ROUND(AVG(delivery_delay_days), 2) AS average_delay_days
FROM gold_orders
WHERE delivery_delay_days IS NOT NULL;


-- QUERY 6: Top 10 states by order volume
SELECT
    customer_state,
    COUNT(*) AS total_orders
FROM gold_orders
GROUP BY customer_state
ORDER BY total_orders DESC
LIMIT 10;
