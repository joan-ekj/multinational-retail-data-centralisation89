/*
You will need to do some work on the products table before casting the data types correctly.

The product_price column has a £ character which you need to remove using SQL.

The team that handles the deliveries would like a new human-readable column added for the weight so they can quickly make decisions on delivery weights.

Add a new column weight_class which will contain human-readable values based on the weight range of the product.

+--------------------------+-------------------+
| weight_class VARCHAR(?)  | weight range(kg)  |
+--------------------------+-------------------+
| Light                    | < 2               |
| Mid_Sized                | >= 2 - < 40       |
| Heavy                    | >= 40 - < 140     |
| Truck_Required           | => 140            |
+----------------------------+-----------------+

*/

 
UPDATE dim_products 
SET product_price = REPLACE(product_price, '£', '');

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(20);

UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck-Required'
END;



/*
+-----------------+--------------------+--------------------+
|  dim_products   | current data type  | required data type |
+-----------------+--------------------+--------------------+
| product_price   | TEXT               | FLOAT              |
| weight          | TEXT               | FLOAT              |
| EAN             | TEXT               | VARCHAR(?)         |
| product_code    | TEXT               | VARCHAR(?)         |
| date_added      | TEXT               | DATE               |
| uuid            | TEXT               | UUID               |
| still_available | TEXT               | BOOL               |
| weight_class    | TEXT               | VARCHAR(?)         |
+-----------------+--------------------+--------------------+
*/


UPDATE dim_products
SET removed = CASE
    WHEN removed = 'Still_avaliable' THEN true
    WHEN removed = 'Removed' THEN false
END;

ALTER TABLE dim_products
  RENAME COLUMN removed TO still_available;

ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT,
    ALTER COLUMN weight TYPE FLOAT,
    ALTER COLUMN "EAN" TYPE VARCHAR(16),
    ALTER COLUMN product_code TYPE VARCHAR(16),
    ALTER COLUMN date_added TYPE DATE,
    ALTER COLUMN weight_class TYPE VARCHAR(20)
    ALTER COLUMN uuid TYPE UUID USING still_available::UUID
    ALTER COLUMN still_available TYPE BOOL USING still_available::BOOL; 

 
ALTER TABLE dim_products
  RENAME COLUMN removed TO still_available;


