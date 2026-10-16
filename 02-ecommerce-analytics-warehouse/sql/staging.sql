-- Staging layer: typed + lightly cleaned mirrors of raw tables

DROP VIEW IF EXISTS stg_customers;
DROP VIEW IF EXISTS stg_products;
DROP VIEW IF EXISTS stg_orders;
DROP VIEW IF EXISTS stg_order_items;

CREATE VIEW stg_customers AS
SELECT
    CAST(customer_id AS INTEGER) AS customer_id,
    TRIM(full_name) AS full_name,
    LOWER(TRIM(email)) AS email,
    TRIM(city) AS city,
    TRIM(state) AS state,
    DATE(created_at) AS created_at
FROM raw_customers
WHERE customer_id IS NOT NULL
  AND email IS NOT NULL;

CREATE VIEW stg_products AS
SELECT
    CAST(product_id AS INTEGER) AS product_id,
    TRIM(product_name) AS product_name,
    TRIM(category) AS category,
    CAST(unit_price AS REAL) AS unit_price
FROM raw_products
WHERE product_id IS NOT NULL
  AND unit_price >= 0;

CREATE VIEW stg_orders AS
SELECT
    CAST(order_id AS INTEGER) AS order_id,
    CAST(customer_id AS INTEGER) AS customer_id,
    DATE(order_date) AS order_date,
    LOWER(TRIM(status)) AS status
FROM raw_orders
WHERE order_id IS NOT NULL
  AND customer_id IS NOT NULL;

CREATE VIEW stg_order_items AS
SELECT
    CAST(order_item_id AS INTEGER) AS order_item_id,
    CAST(order_id AS INTEGER) AS order_id,
    CAST(product_id AS INTEGER) AS product_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(unit_price AS REAL) AS unit_price,
    CAST(quantity AS INTEGER) * CAST(unit_price AS REAL) AS item_revenue
FROM raw_order_items
WHERE order_item_id IS NOT NULL
  AND quantity > 0
  AND unit_price >= 0;
