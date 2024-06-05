import yaml, pandas as pd 
from sqlalchemy import create_engine

class DatabaseConnector: 
     def __init__(self, cred_path=r'C:\Users\ejoan\AiCore_Learning\mrdc\db_creds.yaml'):
      self.cred_path = cred_path
      self.engine = self.init_db_engine()

     def read_db_creds(self):
      with open(self.cred_path, 'r') as db_cred:
        cred = yaml.safe_load(db_cred)
      return cred 
     
     def init_db_engine(self):
       cred = self.read_db_creds()
       db_cred = f"postgresql+psycopg2://{cred['RDS_USER']}:{cred['RDS_PASSWORD']}@{cred['RDS_HOST']}:{cred['RDS_PORT']}/{cred['RDS_DATABASE']}"
       engine = create_engine(db_cred)
       return engine 
     
     def upload_to_db(self, df, table_name):
       #extracted and cleaned use the upload_to_db method to store the data in your sales_data database in a table named dim_users.
       df.to_sql(table_name, self.engine, if_exists='replace')

     
     
    
