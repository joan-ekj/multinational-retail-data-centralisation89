import pandas as pd, numpy as np
import re
from dateutil.parser import parse
from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from pandas.api.types import is_datetime64_dtype

extractor = DataExtractor() # do I need to create an instance of this here?
connector = DatabaseConnector()

class DataCleaning: 
    def __init__(self):
        # self.extractor = DataExtractor() # do I need to create an instance of this here?
        # self.connector = DatabaseConnector()
        pass
        
    def clean_user_data(self):
        user_data = extractor.read_rds_table('legacy_user') # check if required 
        cleaned_user_data = user_data.fillna(np.nan) #replace null values
        cleaned_user_data = cleaned_user_data.replace('', np.nan) #replace missing values 
        cleaned_user_data = cleaned_user_data.dropna()
        cleaned_user_data = cleaned_user_data.reset_index(drop=True)
        #cleaned_user_data = cleaned_user_data.str.strip() #remove trailing and leading spaces 

        #mixed date formats    
        for col in cleaned_user_data.columns:
          if is_datetime64_dtype(cleaned_user_data[col]):
           print(f"Potential date column: {col}")
        
        date_col = 'col'
        cleaned_user_data[date_col] = pd.to_datetime(cleaned_user_data[date_col], format='%d/%m/%Y')

    def clean_card_data(self):
       clean_card_dets = card_details['card_number'].str.replace(r'[^\d]', '', regex=True)
       clean_card_dets = clean_card_dets.replace('', np.nan)
       clean_card_dets = clean_card_dets.fillna(np.nan)
       clean_card_dets = clean_card_dets.dropna() 
       clean_card_dets = clean_card_dets.reset_index(drop=True)
       return clean_card_dets  

    connector.upload_to_db(clean_card_dets, dim_card_details) # does this need to be inside clean_card_data method?
    
    def clean_store_data(self):
       store_data = self. retrieve_stores_data()
       # clean data actions - need to know what data looks like   
       #return clean_store_data

    connector.upload_to_db(clean_store_data, dim_store_details)
    
    @staticmethod
    def clean_weight(weight): 
        pattern1 = r'(\d+)\s*x\s*(\d+\.?\d*)\s*(kg|g|mg|lb|oz|ml|l)'  # Pattern 1: eg. 2 x 50
        pattern2 = r'(\d+\.?\d*)\s*(kg|g|mg|lb|oz|ml|l)'  # Pattern 2: 5g, 20g etc 
        if re.match(pattern1, str(weight)) or re.match(pattern2, str(weight)):
            return weight
        else:
            return np.nan  
    
    @staticmethod
    def convert_to_kg(weight):
        conversion_factors = {
            'kg': 1,
            'g': 0.001,
            'mg': 0.000001,
            'lb': 0.453592,
            'oz': 0.0283495,
            'ml': 0.001, 
            }   

        for unit in conversion_factors:
            if unit in weight:
             try:
                value = float(weight.replace(unit, '').strip())
                return value * conversion_factors[unit]
             except ValueError:
                return np.nan


    def convert_product_weights(self, products_data: pd.DataFrame):
        products_data['weight'] = products_data['weight'].apply(DataCleaning.clean_weight) #is this appropriate? or self.clean_weight
        products_data['weight_kg'] = products_data['weight'].apply(DataCleaning.convert_to_kg)

        return products_data
        
    def clean_products_data(self):
        clean_products_data = products_data.fillna(np.nan) 
        clean_products_data['product_price'] = clean_products_data['product_price'].str.replace(r'^(?!£).*$', '', regex=True)
        clean_products_data['EAN'] = clean_products_data['EAN'].str.replace(r'^(?!\d{13}$).*', '', regex=True)
        clean_products_data['date_added'] = pd.to_datetime(clean_products_data['date_added'], errors ='coerce')
        clean_products_data = clean_products_data.replace('', np.nan)
        clean_products_data = clean_products_data.dropna() 
        clean_products_data = clean_products_data.reset_index(drop=True)

        return clean_products_data

    connector.upload_to_db(clean_products_data, dim_products)

    def clean_orders_data(self):
        orders_data = extractor.read_rds_table('orders_table') # check if required 
        cleaned_orders_data = cleaned_orders_data.drop(columns=['first_name', 'last_name', '1'])
        cleaned_orders_data = orders_data.fillna(np.nan) #replace null values
        cleaned_orders_data = cleaned_orders_data.replace('', np.nan) #replace missing values 
    
        return cleaned_orders_data      
    
    connector.upload_to_db(clean_orders_data, orders_table)

    # mixed_date_df['dates'] = mixed_date_df['mixed_dates'].apply(lambda x: parse(x, fuzzy=True) if pd.notnull(x) else pd.NaT)
    # mixed_date_df['dates'] = pd.to_datetime(mixed_date_df['dates'], errors='coerce')

    def clean_date_data(self):
       #this required - consider dropping rows with invalid date data, drop if year has digits 
       clean_date_data = date_data.fillna(np.nan) 
       clean_date_data = clean_date_data.replace('', np.nan)
       clean_date_data = clean_date_data.dropna()
       clean_date_data = clean_date_data.reset_index(drop=True)

       return clean_date_data
    
    connector.upload_to_db(clean_date_data, dim_date_times)
    

       
       

