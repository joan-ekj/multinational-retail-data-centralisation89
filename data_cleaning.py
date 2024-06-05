import pandas as pd, numpy as np
from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from pandas.api.types import is_datetime64_dtype


class DataCleaning: 
    def __init__(self):
        # self.extractor = DataExtractor() # do I need to create an instance of this here?
        self.connector = DatabaseConnector()
        pass
        
    def clean_user_data(self):
        user_data = self.extractor.read_rds_table("table_name")
        cleaned_user_data = user_data.fillna(np.nan) #replace null values
        cleaned_user_data = cleaned_user_data.replace('', np.nan) #replace missing values 
        cleaned_user_data = cleaned_user_data.str.strip() #remove trailing and leading spaces 

        #mixed date formats    
        for col in cleaned_user_data.columns:
          if is_datetime64_dtype(cleaned_user_data[col]):
           print(f"Potential date column: {col}")
        
        date_col = 'col'
        cleaned_user_data[date_col] = pd.to_datetime(cleaned_user_data[date_col], format='%d/%m/%Y')

    def clean_card_data(self):
       clean_card_dets = card_details[card_number].replace(r'[^\d]', '', regex=True)
       clean_card_dets = clean_card_dets.replace('', np.nan)
       clean_card_dets = clean_card_dets.fillna(np.nan)
       clean_card_dets = clean_card_dets.dropna() 
       return clean_card_dets  
        
       self.connector.upload_to_db(clean_card_dets, dim_card_details)
        