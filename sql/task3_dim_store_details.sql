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


ALTER TABLE dim_store_details
DROP COLUMN lat;


UPDATE dim_store_details
SET country_code = CASE 
    WHEN country_code NOT IN ('GB', 'US', 'DE') THEN NULL
    ELSE country_code
END;

-- should be 441 records 
DELETE FROM dim_store_details
WHERE (address IS NULL
   OR longitude IS NULL
   OR locality IS NULL
   OR store_code IS NULL
   OR staff_numbers IS NULL
   OR opening_date IS NULL
   OR store_type IS NULL
   OR latitude IS NULL
   OR country_code IS NULL
   OR continent IS NULL) 
AND store_code <> 'WEB-1388012W';

ALTER TABLE dim_store_details
    ALTER COLUMN longitude TYPE FLOAT,
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(16),
    ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
    ALTER COLUMN opening_date TYPE DATE,
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN latitude TYPE FLOAT,
    ALTER COLUMN country_code TYPE VARCHAR(2),
    ALTER COLUMN continent TYPE VARCHAR(255);


UPDATE dim_store_details
SET locality = NULL
WHERE store_type = 'Web Portal'; 

