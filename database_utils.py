import yaml
from sqlalchemy import create_engine, inspect

class DatabaseConnector: 
     def __init__(self, creds):
      '''
      This initialises the DatabaseConnector. 

      Args:
        creds (str): File path containing the database credtentials.

      '''
      self.creds = self.read_db_creds(creds)
      self.engine = self.init_db_engine()

     def read_db_creds(self, creds):
      '''
      This method reads the database credentials from a YAML file.
      
      Args:
        creds(str): File path containing the database credtentials.

      Returns: 
        dict: Database credentials.

      '''
      with open(creds, 'r') as db_cred:
        credentials = yaml.safe_load(db_cred)
      return credentials
     
     def init_db_engine(self):
       '''
       This method initialises the SQLAlchemy database engine using the credentials.

       Args:
        None

       Returns:
        engine: SQLAlchemy engine.

       '''
       cred = self.creds
       db_creds = f"postgresql+psycopg2://{cred['USER']}:{cred['PASSWORD']}@{cred['HOST']}:{cred['PORT']}/{cred['DATABASE']}"
       engine = create_engine(db_creds)
       return engine 
     
     def list_db_tables(self): #here or in databasextractions?
       '''
       This method lists all the tables in the database.

       Args: 
        None

       Returns:
        list: List of all the tables in the database

       '''
       inspector = inspect(self.engine)
       tables = inspector.get_table_names()
       print(tables)
       return tables
     
     def upload_to_db(self, df, table_name): 
       '''
       This method uploads a DataFrame to a specified table in the database.

       Args:
        df (pd.DataFrame): DataFrame to be uploaded.
        table_name (str): name of the table in the database.

       Returns:
        None

       '''
       df.to_sql(table_name, self.engine, if_exists='replace')

     
     
    
