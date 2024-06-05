
import pandas as pd 
import tabula
from sqlalchemy import inspect
from database_utils import DatabaseConnector

class DataExtractor:
    def __init__(self):
       self.connector = DatabaseConnector()

    def list_db_tables(self): #here or in databaseconnector?
       engine = self.connector.engine
       inspector = inspect(engine)
       tables = inspector.get_table_names()
       print(tables)
       return tables
    
    def read_rds_table(self, table_name):
       engine = self.connector.engine
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
    
    def list_number_of_stores(self):
       pass