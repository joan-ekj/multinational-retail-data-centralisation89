# Multinational Retail Data Centralisation Project
## Description
This data project forms part of the AiCore Data Engineering Bootcamp. It takes you through a scenario involving the extraction, transformation and loading of retail sales data set. 

At the end of the project, I would have extracted data from various sources, cleaned and centralised retail sales data to a database which can be queried and used for analysis. 
 
## Features 
1. OOP 
2. Pandas 
3. AWS 
4. SQL 

## File Structure 
Py files: 
1. data_cleaning.py: This script contains a class called 'DataCleaning'. The methods within clean and format the raw data extracted from each of the datta sources.  

2. data_extraction.py: This script contains a class called 'DataExtractor'. Within the class are methods defined to extract data from a variety of sources including APIs, an S3 bucket and PDF file.

3. database_utils.py: This script contains a class called 'DatabaseConnector'. The purpose of this class is to connect to the database, cloud and locally and upload cleaned dataset to SQL tables.

SQL files:

These files format the columns in each table, assigning primary keys and foreigns to complete the database design and schema. 


queries - milestone4

These are the queries I ran to answer a number of business scenario questions. 

## Installation

These are required to succesfully run the scripts. 
- Python (pandas, NumPy)
- boto3
- tabula-py
- YAML 
- SQLalchemy 
- pyscopg2
- PostgresSQL 
- python-dateutil
- requests 

