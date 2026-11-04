
-- ============================================
-- E-COMMERCE CUSTOMER ANALYSIS
-- ============================================

-- QUERY 1: Total customers
SELECT
    COUNT(*) AS total_customers
FROM gold_customers;


-- QUERY 2: Customers with multiple orders
SELECT
    COUNT(*) AS repeat_customers
FROM gold_customers
WHERE total_orders > 1;


-- QUERY 3: Top 10 customers by spending
SELECT
    customer_unique_id,
    customer_city,
    customer_state,
    total_orders,
    ROUND(total_spent, 2) AS total_spent
FROM gold_customers
ORDER BY total_spent DESC
LIMIT 10;


-- QUERY 4: Customers by state
SELECT
    customer_state,
    COUNT(*) AS total_customers
FROM gold_customers
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;


-- QUERY 5: Average customer spending
SELECT
    ROUND(AVG(total_spent), 2) AS average_customer_spending
FROM gold_customers;


-- QUERY 6: One-time customers
SELECT
    COUNT(*) AS one_time_customers
FROM gold_customers
WHERE total_orders = 1;
