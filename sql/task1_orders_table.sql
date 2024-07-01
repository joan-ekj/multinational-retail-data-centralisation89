-- Change the data types to correspond to those seen in the table below.
/*
+------------------+--------------------+--------------------+
|   orders_table   | current data type  | required data type |
+------------------+--------------------+--------------------+
| date_uuid        | TEXT               | UUID               |
| user_uuid        | TEXT               | UUID               |
| card_number      | TEXT               | VARCHAR(?)         |
| store_code       | TEXT               | VARCHAR(?)         |
| product_code     | TEXT               | VARCHAR(?)         |
| product_quantity | BIGINT             | SMALLINT           |
+------------------+--------------------+--------------------+
*/

ALTER TABLE orders_table
    ALTER COLUMN card_number TYPE VARCHAR(20),
    ALTER COLUMN store_code TYPE VARCHAR(16),
    ALTER COLUMN product_code TYPE VARCHAR(16),
    ALTER COLUMN product_quantity TYPE SMALLINT,
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;

