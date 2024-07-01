-- Task 1). How many stores does the business have and in which countries?
SELECT dim_store_details.country_code AS country, COUNT(dim_store_details.store_code) AS total_no_stores
FROM dim_store_details
GROUP BY dim_store_details.country_code;

-- Task 2). Which locations currently have the most stores?
SELECT dim_store_details.locality, COUNT(dim_store_details.store_code) AS total_no_stores
FROM dim_store_details
GROUP BY dim_store_details.locality
ORDER BY total_no_stores DESC
LIMIT 7;

-- Task 3). Which months produced the largest amount of sales? 
SELECT ROUND(SUM(orders_table.product_quantity * dim_products.product_price)::NUMERIC, 2) AS total_sales,
       dim_date_times.month
FROM orders_table
JOIN dim_products USING (product_code)
JOIN dim_date_times USING (date_uuid)
GROUP BY dim_date_times.month
ORDER BY total_sales DESC
LIMIT 6;

-- Task 4). How many sales are coming from online?
ALTER TABLE dim_store_details
ADD COLUMN location VARCHAR(6);

UPDATE dim_store_details
SET location = CASE
    WHEN store_type = 'Web Portal' THEN 'Web'
    ELSE 'Offline'
END;

SELECT dim_store_details.location, 
       SUM(orders_table.product_quantity) AS product_quantity_count, 
       COUNT(orders_table.product_quantity) AS number_of_sales
FROM orders_table
JOIN dim_store_details USING (store_code)
GROUP BY dim_store_details.location;

-- Task 5). What perecentage of sales came through each type of store?

WITH total_sales_cte AS (
    SELECT SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales
    FROM orders_table
    JOIN dim_products USING (product_code)
)

SELECT dim_store_details.store_type, 
       ROUND(SUM(orders_table.product_quantity * dim_products.product_price)::NUMERIC, 2) AS store_sales,
       ROUND((SUM(orders_table.product_quantity * dim_products.product_price) / total_sales_cte.total_sales * 100):: NUMERIC, 2) AS perecentage_total(%)  
FROM orders_table
JOIN dim_products USING (product_code)
JOIN dim_store_details USING (store_code)
CROSS JOIN total_sales_cte
GROUP BY dim_store_details.store_type, total_sales_cte.total_sales;

/*SELECT dim_store_details.store_type, SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales
FROM orders_table
JOIN dim_products USING (product_code)
JOIN dim_store_details USING(store_code)
GROUP BY store_type;*/

--Task 6). Which month in each year produced the highest cost of sales?
SELECT dim_date_times.month, 
       dim_date_times.year, 
       ROUND(SUM(orders_table.product_quantity * dim_products.product_price):: NUMERIC, 2) AS total_sales
FROM orders_table
JOIN dim_products USING (product_code)
JOIN dim_date_times USING (date_uuid)
GROUP BY dim_date_times.month, 
         dim_date_times.year
ORDER BY total_sales DESC
LIMIT 10; 

-- Task 7). What is your staff headcount?
SELECT SUM(dim_store_details.staff_numbers) AS total_staff_numbers, 
       dim_store_details.country_code
FROM dim_store_details
GROUP BY dim_store_details.country_code
ORDER BY total_staff_numbers DESC;

-- Task 8). Which German store type is selling the most?
SELECT ROUND(SUM(orders_table.product_quantity * dim_products.product_price):: NUMERIC, 2) AS total_sales,
       dim_store_details.store_type,
       dim_store_details.country_code
FROM orders_table 
JOIN dim_products USING (product_code)
JOIN dim_store_details USING (store_code)
WHERE dim_store_details.country_code = 'DE'
GROUP BY dim_store_details.store_type, dim_store_details.country_code;

-- Task 9). How quickly is the company making sales?
-- change timestamp to TIME - currently TEXT 

		
WITH date_times AS (
SELECT year,
       month,
       day,
       timestamp,
       TO_TIMESTAMP(CONCAT(year, '/', month, '/', day, '/', timestamp), 'YYYY/MM/DD/HH24:MI:ss') as times
FROM dim_date_times 
ORDER BY times DESC),		   	


next_times AS(
SELECT year,
       timestamp,
       times,
LEAD(times) OVER(ORDER BY times DESC) AS next_times
FROM date_times),

avg_times AS(
SELECT year,
       (AVG(times - next_times)) AS avg_times
FROM next_times
GROUP BY year
ORDER BY avg_times DESC)

SELECT year,
	CONCAT('"Hours": ', (EXTRACT(HOUR FROM avg_times)),','
	' "minutes" :', (EXTRACT(MINUTE FROM avg_times)),','
    ' "seconds" :', ROUND(EXTRACT(SECOND FROM avg_times)),','
    ' "milliseconds" :', ROUND((EXTRACT( SECOND FROM avg_times)- FLOOR(EXTRACT(SECOND FROM avg_times)))*100))
	
   as actual_time_taken

FROM avg_times
GROUP BY year, avg_times
ORDER BY avg_times DESC
LIMIT 5;