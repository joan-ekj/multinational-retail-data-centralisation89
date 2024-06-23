import yaml
from sqlalchemy import create_engine, inspect

class DatabaseConnector: 
     def __init__(self): #=r'C:\Users\ejoan\AiCore_Learning\mrdc\db_creds.yaml'
      self.creds = self.read_db_creds(creds)
      self.engine = self.init_db_engine()

     def read_db_creds(self, creds):
      '''
      This method reads the database credentials from a file and returns a dictionary of the credentials.
      
      Args:
        creds: File path containing the database credtentials 

      Returns: 
        database credentials in a dictionary

      '''
      with open(creds, 'r') as db_cred:
        credentials = yaml.safe_load(db_cred)
      return credentials
     
     def init_db_engine(self):
       '''
       This method reads the credentials from the return of read_db_creds, initialises and returns a sqlalchemy database engine.

       Args:
        None

       Returns:
        a sqlalchemy engine 

       '''
       cred = self.creds
       db_creds = f"postgresql+psycopg2://{cred['USER']}:{cred['PASSWORD']}@{cred['HOST']}:{cred['PORT']}/{cred['DATABASE']}"
       engine = create_engine(db_creds)
       return engine 
     
     def list_db_tables(self): #here or in databasextractions?
       '''
       This method uses the engine and lists all the tables in the database.

       Args: 
        None

       Returns:
        a list of all the tables in the database

       '''
       inspector = inspect(self.engine)
       tables = inspector.get_table_names()
       print(tables)
       return tables
     
     def upload_to_db(self, df, table_name): # needs to upload to local db instead 
       #extracted and cleaned use the upload_to_db method to store the data in your sales_data database in a table named dim_users.
       '''
       This function uploads a dataframe to a specified table in the database.

       Args:
        df (pd.DataFrame): pandas DataFrame to be uploaded.
        table_name (str): name of the table in the database.

       Returns:
        None

       '''
       df.to_sql(table_name, self.engine, if_exists='replace')

     
     
    
