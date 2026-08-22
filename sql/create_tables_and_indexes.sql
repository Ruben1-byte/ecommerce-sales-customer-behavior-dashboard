-- Set order_id sebagai Primary Key
ALTER TABLE sales ADD PRIMARY KEY (order_id);

-- Buat indeks untuk kolom yang sering digunakan di klausa WHERE dan GROUP BY
ALTER TABLE sales ADD INDEX idx_order_date (order_date);
ALTER TABLE sales ADD INDEX idx_category (category);
ALTER TABLE sales ADD INDEX idx_payment_status (payment_status);