/*
There are two latitude columns in the store details table. Using SQL, merge one of the columns into the other so you have one latitude column. -- lat and latitude
lat was basically null so have dropped instead 

Then set the data types for each column as shown below:

+---------------------+-------------------+------------------------+
| store_details_table | current data type |   required data type   |
+---------------------+-------------------+------------------------+
| longitude           | TEXT              | FLOAT                  |
| locality            | TEXT              | VARCHAR(255)           |
| store_code          | TEXT              | VARCHAR(?)             |
| staff_numbers       | TEXT              | SMALLINT               |
| opening_date        | TEXT              | DATE                   |
| store_type          | TEXT              | VARCHAR(255) NULLABLE  |
| latitude            | TEXT              | FLOAT                  |
| country_code        | TEXT              | VARCHAR(?)             |
| continent           | TEXT              | VARCHAR(255)           |
+---------------------+-------------------+------------------------+

There is a row that represents the business's website change the location column values from N/A to NULL.

*/

-- do I really need? Could just drop lat instead as lat hasn nothing important 

UPDATE dim_store_details
SET latitude = lat
WHERE store_type = 'Web Portal';

ALTER TABLE dim_store_details
DROP COLUMN lat;


ALTER TABLE dim_store_details
    ALTER COLUMN longitude TYPE FLOAT,
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(16),
    ALTER COLUMN staff_numbers TYPE SMALLINT,
    ALTER COLUMN opening_date TYPE DATE,
    ALTER COLUMN store_type TYPE VARCHAR(255) NULLABLE,
    ALTER COLUMN latitude TYPE FLOAT,
    ALTER COLUMN country_code TYPE VARCHAR(2),
    ALTER COLUMN continent TYPE VARCHAR(255);

UPDATE store_details_table
SET locality = NULL
WHERE store_type = 'Web Portal'; 