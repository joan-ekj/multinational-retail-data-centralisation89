
import pandas as pd 
import tabula
import requests
import boto3
from sqlalchemy import inspect
from database_utils import DatabaseConnector

connector = DatabaseConnector() # removed from constructor 

class DataExtractor:
    def __init__(self):
          pass
       

    def list_db_tables(self): #here or in databaseconnector?
       engine = connector.engine
       inspector = inspect(engine)
       tables = inspector.get_table_names()
       print(tables)
       return tables
    
    def read_rds_table(self, table_name):
       engine = connector.engine
       user_data = pd.read_sql_query('''SELECT * FROM "{table_name}"''', engine)
       print(user_data)
       return user_data
       

       #table_name = input('enter table name')
       #It will take in an instance of your DatabaseConnector class and the table name as an argument and return a pandas DataFrame.
       #Use your list_db_tables method to get the name of the table containing user data.
       #Use the read_rds_table method to extract the table containing user data and return a pandas DataFrame.

    def retrieve_pdf_data(self, pdf_path):
       #pdf_path = r'C:\Users\ejoan\AiCore_Learning\mrdc\card_details.pdf' - avoid hard coding 
       card_details = tabula.read_pdf(pdf_path, stream=True)
       return card_details 
    
    def list_number_of_stores(self): # It should take in the number of stores endpoint and header dictionary as an argument
        url = r'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
        headers = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDM'}
      
        response = requests.get(url, headers=headers)
        data = response.json()
        number_stores = data['number_stores']
        return number_stores
   

    def retrieve_stores_data(self, number_stores): # will take the retrieve a store endpoint as an argument and extracts all the stores from the API saving them in a pandas DataFrame
        url = f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{number_stores}'
        headers = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDM'}
      
        response = requests.get(url, headers=headers)
        data = response.json()
        store_data =  pd.read_json(data)
        return store_data
    
    def extract_from_s3(self, s3_url):
        #r's3://data-handling-public/products.csv'
        #https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json.
        s3 = boto3.client('s3')

        if 's3://' in s3_url:
            bucket_name, object_key = s3_url.replace("s3://", "").split("/", 1)
        elif 'https' in s3_url:
            bucket_name, object_key = s3_url.replace("https://", "").split("/", 1)

        if 'csv' in object_key:
            s3.download_file(bucket_name, object_key, 'products.csv')
            products_data = pd.read_csv('products.csv')
            return products_data 
        elif '.json' in object_key:
            s3.download_file(bucket_name, object_key, 'date_details.json')
            date_data = pd.read_json('date_details.json')
            return date_data



if __name__ == '__main__':
    pass
