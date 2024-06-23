import pandas as pd, numpy as np, re, phonenumbers
from phonenumbers import NumberParseException
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

    def clean_null_and_empty(self, df: pd.DataFrame):
        '''
        This method takes a DataFrame, replaces null values and empty strings with np.nan, and resets the index.

        Args:
         df (pd.DataFrame): a pandas DataFrame containing the column to clean.

        Returns:
         pd.DataFrame: a cleaned dataframe with - do I need to return?

        '''
        df = df.fillna(np.nan)  # Replace null values with np.nan
        df = df.replace('', np.nan)  # Replace empty strings with np.nan
        df = df.dropna(how='all')  # Drop rows where all entries are nan
        df = df.reset_index(drop=True)  # Reset index
        return df
    
    def parse_dates(self, df, column_name):
        '''
        This method converts date-like strings in a specified column of a DataFrame to datetime objects.

        Args:
         df (pd.DataFrame): a pandas DataFrame
         column_name (str): The name of the column with dates.
 

        Returns:
         pd.DataFrame: the DataFrame with the specified column parsed as dates.

        '''
        df[column_name] = df[column_name].apply(lambda x: parse(x, fuzzy=True) if pd.notnull(x) else pd.NaT) #fuzzy=True allows non-date characters to be parsed
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce') # errors=coerce ensures unparseable dates are converted to 'NaT'
        return df
    
    def clean_phone_numbers(self, df, column_name):
        '''
        Cleans and formats phone numbers in a DataFrame column, returning a new DataFrame.

        Args:
         df (pd.DataFrame): The DataFrame containing the phone numbers.
         column_name (str): The name of the column with phone numbers.

        Returns:
         pd.DataFrame: New DataFrame with cleaned and formatted phone numbers.
        '''
        
        def format_phone_number(phone):
            try:
                parsed_number = phonenumbers.parse(phone)
                if phonenumbers.is_valid_number(parsed_number):
                    return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                else:
                    return np.nan
            except phonenumbers.NumberParseException:
                return np.nan
            
        df[column_name] = df[column_name].apply(format_phone_number)
        return df 

    def replace_if_contains_digits(self, df, column_name):
        '''
        This method cleans the name data columns.

        Args: 
         df (pd.DataFrame): The DataFrame containing names.
         column_name (str): The name of the column with names - first or last.

        Returns: 
         pd.DataFrame: DataFrame with cleaned user names.

        '''
        df[column_name] = df[column_name].apply(lambda text: re.sub(r'\d', '', text))

        return df
    
    def clean_staff_num(self, df, column_name):
        '''
        This method cleans the staff_number column.

        Args: 
         df (pd.DataFrame): The DataFrame containing staff number.
         column_name (str): The name of the column with staff number.

        Returns: 
         pd.DataFrame: DataFrame with cleaned staff number.

        '''
        if len(column_name) > 3:
            return ''
        
        df[column_name] = df[column_name].apply(lambda x: re.sub(r'\D', '')) #replace non-digits with ''
        return df

        
    def clean_user_data(self):
        '''
        This method cleans the user data.

        Args: 
         none

        Returns: 
         pd.DataFrame: DataFrame with cleaned user data.

        '''
        user_data = extractor.read_rds_table('legacy_user') # check if required, maybe add the dataframe as an argument?
        cleaned_user_data = self.parse_dates(cleaned_user_data, 'date_of_birth')
        cleaned_user_data = self.parse_dates(cleaned_user_data, 'join_date')
        cleaned_user_data = self.clean_phone_numbers(cleaned_user_data, 'phone')
        cleaned_user_data = self.replace_if_contains_digits(cleaned_user_data, 'first_name')
        cleaned_user_data = self.replace_if_contains_digits(cleaned_user_data, 'last_name')
        cleaned_user_data = cleaned_user_data['country_code'].str.replace({'GGB': 'GB'})
        cleaned_user_data = cleaned_user_data['country'].apply(lambda x: '' if x not in ['Germany', 'United Kingdom', 'United States'] else x)
        cleaned_user_data = self.clean_null_and_empty(user_data)

        return cleaned_user_data
    
    connector.upload_to_db(cleaned_user_data, dim_users) # do I need this here?

    def clean_card_data(self):
        '''
        This method cleans the card details.

        Args: 
         none

        Returns: 
         pd.DataFrame: DataFrame with cleaned card details. 

        '''
        clean_card_dets = card_details['card_number'].str.replace(r'[^\d]', '', regex=True) #do I need to load card details data here like user data?
        clean_card_dets = self.clean_null_and_empty(clean_card_dets)
       
        return clean_card_dets  

    connector.upload_to_db(clean_card_dets, dim_card_details) # does this need to be inside clean_card_data method?
    
    def clean_store_data(self):
        '''
        This method cleans the store data.

        Args: 
         None 

        Returns: 
         pd.DataFrame: DataFrame with cleaned store data.

        '''
        store_data = self.retrieve_stores_data() #required?
        clean_store_data['continent'] = store_data['continent'].str.replace({'eeEurope': 'Europe', 'eeAmerica': 'America'})
        clean_store_data['continent'] = clean_store_data['continent'].apply(lambda x: '' if x not in ['America', 'Europe'] else x)
        # clean_store_data = clean_store_data.drop(columns=['lat']) 
        clean_store_data = self.parse_dates(clean_store_data, 'opening_date')
        clean_store_data['longitude'] = pd.to_numeric(clean_store_data['longitude'], errors='coerce')
        clean_store_data['latitude'] = pd.to_numeric(clean_store_data['latitude'], errors='coerce')
        clean_store_data =  self.clean_staff_num(clean_store_data, 'staff_numbers')
        clean_store_data = self.clean_null_and_empty(clean_store_data)
        
        return clean_store_data

    connector.upload_to_db(clean_store_data, dim_store_details)

    @staticmethod
    def clean_weight(weight): 
        pattern1 = r'(\d+)\s*x\s*(\d+\.?\d*)\s*(kg|g|mg|lb|oz|ml|l)'  # Pattern 1: eg. 2 x 50 - need to define function to address this as currently ignored 
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
                if 'x' in weight:
                    quantity, value = weight.split('x')
                    quantity = float(quantity)
                    value = float(value.replace(unit, '').strip()) #strip handles spaces
                    return quantity * value * conversion_factors[unit]
                else:
                    value = float(weight.replace(unit, '').strip()) 
                    return value * conversion_factors[unit]
             except ValueError:
                return np.nan


    def convert_product_weights(self, products_data: pd.DataFrame):
        '''
        This method cleans and converts the weight column to float in kg.

        Args: 
         df: products data DataFrame

        Returns: 
         pd.DataFrame: pandas DataFrame with cleaned weight column.

        '''
        products_data['weight'] = products_data['weight'].apply(DataCleaning.clean_weight) #is this appropriate? or self.clean_weight
        products_data['weight_kg'] = products_data['weight'].apply(DataCleaning.convert_to_kg)

        return products_data
        
    def clean_products_data(self, products_data: pd.DataFrame):
        '''
        This method cleans the products data.

        Args: 
         products_data: pd.DataFrame containing products data.

        Returns: 
         pd.DataFrame: cleaned products data in pandas DataFrame.

        '''
        clean_products_data['product_price'] = products_data['product_price'].str.replace(r'^(?!£).*$', '', regex=True) #if there's no £ in the string, replace with ''
        clean_products_data['EAN'] = clean_products_data['EAN'].str.replace(r'^(?!\d{13}$).*', '', regex=True) # if not 13 digits, replace with ''
        #clean_products_data = self.parse_dates(clean_products_data['date_added'], errors ='coerce')

        clean_products_data = self.clean_null_and_empty(clean_products_data)
        clean_products_data = self.parse_dates(clean_products_data, 'date_added')

        return clean_products_data

    connector.upload_to_db(clean_products_data, dim_products)

    def clean_orders_data(self):
        '''
        This method cleans the orders table data.

        Args: 
         products_data: pd.DataFrame containing products data # orders_data as an argument

        Returns: 
         cleaned orders data in pandas DataFrame.

        '''
        orders_data = extractor.read_rds_table('orders_table') # read or take in as an argument
        cleaned_orders_data = cleaned_orders_data.drop(columns=['first_name', 'last_name', '1']) #drop these columns
        cleaned_orders_data= self.clean_null_and_empty(cleaned_orders_data)
    
        return cleaned_orders_data      
    
    connector.upload_to_db(clean_orders_data, orders_table)

    def clean_date_data(self):
       #this required - consider dropping rows with invalid date data, drop if year has digits 
       clean_date_data = self.clean_null_and_empty(date_data)

       #clean_date_data = date_data.fillna(np.nan) 
       #clean_date_data = clean_date_data.replace('', np.nan)
       #clean_date_data = clean_date_data.dropna()
       #clean_date_data = clean_date_data.reset_index(drop=True)

       return clean_date_data
    
    connector.upload_to_db(clean_date_data, dim_date_times)
    

       
       

