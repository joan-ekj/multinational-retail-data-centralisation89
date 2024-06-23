/*

Now that the tables have the appropriate data types we can begin adding the primary keys to each of the tables prefixed with dim.

Each table will serve the orders_table which will be the single source of truth for our orders.

Check the column header of the orders_table you will see all but one of the columns exist in one of our tables prefixed with dim.

We need to update the columns in the dim tables with a primary key that matches the same column in the orders_table.

Using SQL, update the respective columns as primary key columns.
*/

-- Dim-Users 
-- make user_uuid PK 
ALTER TABLE dim_users
ADD PRIMARY KEY (user_uuid);

-- Dim-Store-Details
-- make store_code PK
ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);

-- Dim-Products
-- products_code PK 
ALTER TABLE dim_products
ADD PRIMARY KEY (products_code); -- need to update product code in orders to all caps 

--Dim-Date-Times
-- date_uuid PK 
ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);

-- Dim-Card-Details
-- card_number PK
ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);