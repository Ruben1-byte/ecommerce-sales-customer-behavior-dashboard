-- ===================================================
-- E-COMMERCE SALES & CUSTOMER BEHAVIOR ANALYTICAL QUERIES
-- ===================================================

-- Query 1: Top 3 Produk Terlaris di Setiap Kategori (Window Function)
WITH product_rankings AS (
    SELECT 
        category,
        product_name,
        SUM(quantity) AS total_quantity_sold,
        SUM(total_sales) AS total_revenue_generated,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY SUM(quantity) DESC) AS rank_position
    FROM sales
    GROUP BY category, product_name
)
SELECT 
    category,
    product_name,
    total_quantity_sold,
    total_revenue_generated
FROM product_rankings
WHERE rank_position <= 3
ORDER BY category, rank_position;


-- Query 2: Tren Penjualan Bulanan & Pertumbuhan MoM (LAG Function)
WITH monthly_perf AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS month_year,
        SUM(total_sales) AS total_revenue,
        COUNT(order_id) AS total_orders
    FROM sales
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    month_year,
    total_orders,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY month_year) AS prev_month_revenue,
    ROUND(
        ((total_revenue - LAG(total_revenue) OVER (ORDER BY month_year)) / LAG(total_revenue) OVER (ORDER BY month_year)) * 100, 
        2
    ) AS mom_growth_percent
FROM monthly_perf;


-- Query 3: Performa Metode Pembayaran (Aggregation)
SELECT 
    payment_method,
    COUNT(order_id) AS total_transactions,
    SUM(total_sales) AS total_revenue,
    ROUND(AVG(total_sales), 2) AS avg_transaction_value
FROM sales
GROUP BY payment_method
ORDER BY total_revenue DESC;