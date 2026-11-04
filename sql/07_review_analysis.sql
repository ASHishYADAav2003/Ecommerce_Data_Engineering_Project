-- 1. Total number of reviews
SELECT
    COUNT(*) AS total_reviews
FROM gold_reviews;


-- 2. Review score distribution
SELECT
    review_score,
    COUNT(*) AS review_count
FROM gold_reviews
GROUP BY review_score
ORDER BY review_score;


-- 3. Reviews by category
SELECT
    review_category,
    COUNT(*) AS review_count
FROM gold_reviews
GROUP BY review_category
ORDER BY review_count DESC;


-- 4. Average review score
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM gold_reviews;


-- 5. Average review response time
SELECT
    ROUND(AVG(review_response_days), 2) AS avg_response_days
FROM gold_reviews
WHERE review_response_days IS NOT NULL;


-- 6. Reviews by order status
SELECT
    order_status,
    COUNT(*) AS review_count
FROM gold_reviews
GROUP BY order_status
ORDER BY review_count DESC;