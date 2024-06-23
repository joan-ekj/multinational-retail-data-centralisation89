/*
Make the associated changes after finding out what the lengths of each variable should be:

+------------------------+-------------------+--------------------+
|    dim_card_details    | current data type | required data type |
+------------------------+-------------------+--------------------+
| card_number            | TEXT              | VARCHAR(?)         |
| expiry_date            | TEXT              | VARCHAR(?)         |
| date_payment_confirmed | TEXT              | DATE               |
+------------------------+-------------------+--------------------+
*/

ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(20),
    ALTER COLUMN expiry_date TYPE VARCHAR(4),
    ALTER COLUMN date_payment_confirmed TYPE DATE;