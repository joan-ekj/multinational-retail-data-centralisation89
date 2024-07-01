--The column required to be changed in the users table are as follows:
/* +----------------+--------------------+--------------------+
| dim_users      | current data type  | required data type |
+----------------+--------------------+--------------------+
| first_name     | TEXT               | VARCHAR(255)       |
| last_name      | TEXT               | VARCHAR(255)       |
| date_of_birth  | TEXT               | DATE               |
| country_code   | TEXT               | VARCHAR(?)         |
| user_uuid      | TEXT               | UUID               |
| join_date      | TEXT               | DATE               |
+----------------+--------------------+--------------------+


*/ 
-- should be 15284 records 
DELETE FROM dim_users
WHERE first_name IS NULL
   OR last_name IS NULL
   OR date_of_birth IS NULL
   OR company IS NULL
   OR email_address IS NULL
   OR address IS NULL
   OR country IS NULL
   OR country_code IS NULL
   OR join_date IS NULL
   OR user_uuid IS NULL;


-- alter remaining columns as usual    
ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255),
    ALTER COLUMN last_name TYPE VARCHAR(255),
    ALTER COLUMN date_of_birth TYPE DATE,
    ALTER COLUMN country_code TYPE VARCHAR(2),
    ALTER COLUMN join_date TYPE DATE,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;
