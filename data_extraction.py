
import pandas as pd 
import tabula
import requests
import boto3


class DataExtractor:
    def read_rds_table(self, engine, table_name): 
       '''
       This method extracts the database table to a pandas DataFrame.
       
       Args:
        engine: The SQLAlchemy engine from DatabaseConnector class.
        table_name (str): Name of the table to read from the database. 

       Returns: 
          pd.DataFrame: DataFrame containing the specified table data.

       '''
       query = f'SELECT * FROM "{table_name}"'
       user_data = pd.read_sql_query(query, engine)
       print(user_data)
       return user_data

    def retrieve_pdf_data(self, pdf_path):
       '''
       This method extracts all the pages of a PDF document to a pandas DataFrame.

       Args:
        pdf_path (str): File path to the PDF 

        Returns:
          pd.DataFrame: DataFrame containing the card details data.

       '''
       card_details = tabula.read_pdf(pdf_path, stream=False, pages='all')
       return card_details 
    
    def list_number_of_stores(self, url, headers):
        '''
        This method returns the number of stores in the business.

        Args: 
         url (str): Endpoint URL for the number of stores. 
         headers (dict): Headers for the API request

        Returns: 
         the number of stores.

        '''
        response = requests.get(url, headers=headers)
        data = response.json()
        number_stores = data['number_stores']
        print(number_stores)
        return number_stores
   

    def retrieve_stores_data(self, url, headers): # will take the retrieve a store endpoint as an argument and extracts all the stores from the API saving them in a pandas DataFrame
        '''
        This method extracts all the stores data from the API and saves them in a pandas DataFrame

        Args: 
         url (str): Endpoint URL for the store details.
         headers (dict): Headers for the API request.

        Returns: 
          pd.DataFrame: DataFrame with store data.

        '''
        result = []
        number_stores = 451
    
        for store_number in range(number_stores):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status() # checks if request was successful
                result.append(pd.json_normalize(response.json()))
            except requests.exceptions.RequestException as e:
                print(f"Error fetching store {store_number}: {e}")
    
        store_data = pd.concat(result, ignore_index=True)
        return store_data

    
    def extract_from_s3(self, s3_url):
        '''
        This method extracts data from an S3 bucket.

        Args: 
         s3_url (str): S3 URL to the object.

        Returns:
         pd.DataFrame: DataFrame containing the data from the S3 objects. 

        '''
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
        else:
            raise ValueError("Unsupported file format")


