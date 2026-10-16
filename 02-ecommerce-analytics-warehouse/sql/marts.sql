-- Marts / presentation layer

DROP TABLE IF EXISTS fact_order_items;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS mart_daily_revenue;

CREATE TABLE dim_customer AS
SELECT
    customer_id,
    full_name,
    email,
    city,
    state,
    created_at
FROM stg_customers;

CREATE TABLE dim_product AS
SELECT
    product_id,
    product_name,
    category,
    unit_price
FROM stg_products;

CREATE TABLE fact_order_items AS
SELECT
    i.order_item_id,
    i.order_id,
    o.order_date,
    o.customer_id,
    i.product_id,
    i.quantity,
    i.unit_price,
    i.item_revenue,
    o.status
FROM stg_order_items i
JOIN stg_orders o ON o.order_id = i.order_id
WHERE o.status IN ('paid', 'shipped', 'delivered');

CREATE TABLE mart_daily_revenue AS
SELECT
    order_date AS date,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(*) AS items_sold,
    SUM(quantity) AS units,
    ROUND(SUM(item_revenue), 2) AS revenue
FROM fact_order_items
GROUP BY order_date
ORDER BY order_date;
