/*
With the primary keys created in the tables prefixed with dim we can now create the foreign keys in the orders_table to reference the primary keys in the other tables.

Use SQL to create those foreign key constraints that reference the primary keys of the other table.

This makes the star-based database schema complete.

*/

/*
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_users
FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid),
ADD CONSTRAINT fk_orders_store
FOREIGN KEY (store_code) REFERENCES dim_store_details (store_code),
ADD CONSTRAINT fk_orders_products
FOREIGN KEY (product_code) REFERENCES dim_products(product_code),
ADD CONSTRAINT fk_orders_date
FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid),
ADD CONSTRAINT fk_orders_card
FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);

*/ 

-- orders table + store_details - worked
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_store
FOREIGN KEY (store_code) REFERENCES dim_store_details (store_code);

-- orders table + products - worked
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_products
FOREIGN KEY (product_code) REFERENCES dim_products(product_code)

-- orders table + date_times  - worked 
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_date
FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid)

-- orders table + card_details - difference 
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_card
FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);

--orders table + dim_users - worked  
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_users
FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);