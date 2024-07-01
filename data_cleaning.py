import pandas as pd
import numpy as np
import re
import phonenumbers
from phonenumbers import NumberParseException
from dateutil.parser import parse
# from pandas.api.types import is_datetime64_dtype

class DataCleaning: 
    def clean_null_and_empty(self, df):
        '''
        This method cleans nulls in a DataFrame.

        Args:
         df (pd.DataFrame): a pandas DataFrame containing columns to clean.

        Returns:
         pd.DataFrame: a cleaned DataFrame with nulls and empty strings handled. 

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
        def try_parse_date(x):
            try:
                return parse(x, fuzzy=True) #fuzzy=True allows non-date characters to be parsed
            except (ValueError, TypeError):
                return pd.NaT

        #apply try_parse_date, if not null return date else NaT  
        df[column_name] = df[column_name].apply(lambda x: try_parse_date(x) if pd.notnull(x) else pd.NaT) 
        # errors=coerce ensures unparseable dates are converted to 'NaT'
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
        return df
    
    def clean_expiry_date(self, df, column_name):
        '''
        This method cleans the expiry date column in specified DataFrame.

        Args:
         df (pd.DataFrame): a pandas DataFrame
         column_name (str): The name of the column with dates.
 

        Returns:
         pd.DataFrame: the DataFrame with cleaned expiry date column.

        ''' 
        df[column_name] = df[column_name].astype(str)
        df[column_name] = df[column_name].apply(lambda x: x if len(x) <6 else np.nan)
        return df

    
    def clean_phone_numbers(self, df, column_name):
        '''
        This method cleans and formats phone numbers in a DataFrame column.

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
        df[column_name] = df[column_name].astype(str).fillna('')
        df[column_name] = df[column_name].apply(lambda x: re.sub(r'\d', '', x))
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
        df[column_name] = df[column_name].astype(str)
        df[column_name] = df[column_name].apply(lambda x: re.sub(r'\D', '', x))
        df[column_name] = df[column_name].apply(lambda x: x if len(x) <= 3 else np.nan)
        return df 

        
    def clean_user_data(self, user_data):
        '''
        This method cleans the user data.

        Args: 
         user_data (pd.DataFrame): DataFrame containing user data.

        Returns: 
         pd.DataFrame: DataFrame with cleaned user data.

        '''
        user_data = self.parse_dates(user_data, 'date_of_birth')
        user_data = self.parse_dates(user_data, 'join_date')
        user_data = self.clean_phone_numbers(user_data, 'phone_numbers')
        user_data = self.replace_if_contains_digits(user_data, 'first_name')
        user_data = self.replace_if_contains_digits(user_data, 'last_name')
        user_data['country_code'] = user_data['country_code'].replace('GGB', 'GB')
        user_data = user_data['country'].apply(lambda x: '' if x not in ['Germany', 'United Kingdom', 'United States'] else x)
        user_data = self.clean_null_and_empty(user_data)

        return user_data

    def clean_card_data(self, card_details):
        '''
        This method cleans the card details.

        Args: 
         card_details (pd.DataFrame): DataFrame containing card details.

        Returns: 
         pd.DataFrame: DataFrame with cleaned card details. 

        '''
        card_details = card_details['card_number'].replace(r'[^\d]', '', regex=True)
        card_details = self.clean_expiry_date(card_details, 'expiry_date') 
        card_details = self.parse_dates(card_details, 'date_payment_confirmed')
        # card_details = self.clean_null_and_empty(card_details)
       
        return card_details 
 
    def clean_store_data(self, store_data):
        '''
        This method cleans the store data.

        Args: 
         store_data (pd.DataFrame): DataFrame containing store data.

        Returns: 
         pd.DataFrame: DataFrame with cleaned store data.

        '''
        store_data['continent'] = store_data['continent'].replace({'eeEurope': 'Europe', 'eeAmerica': 'America'})
        store_data['continent'] = store_data['continent'].apply(lambda x: '' if x not in ['America', 'Europe'] else x)
        store_data['country_code'] = store_data['country_code'].apply(lambda x: '' if x not in ['GB', 'US', 'DE'] else x)
        store_data = self.parse_dates(store_data, 'opening_date')
        store_data =  self.clean_staff_num(store_data, 'staff_numbers')
        store_data['longitude'] = pd.to_numeric(store_data['longitude'], errors='coerce')
        store_data['latitude'] = pd.to_numeric(store_data['latitude'], errors='coerce')
        clean_store_data = self.clean_null_and_empty(clean_store_data)
        
        return store_data

    @staticmethod
    def clean_weight(weight): 
        '''
        This method validates the weight format in the product data.

        Args:
         weight (str): A string representing the weight.

        Returns:
         str or NaN: The original weight string if valid, else NaN.

        '''
        pattern1 = r'(\d+)\s*x\s*(\d+\.?\d*)\s*(kg|g|mg|lb|oz|ml|l)'  # Pattern 1: eg. 2 x 50 - need to define function to address this as currently ignored 
        pattern2 = r'(\d+\.?\d*)\s*(kg|g|mg|lb|oz|ml|l)'  # Pattern 2: 5g, 20g etc 
        if re.match(pattern1, str(weight)) or re.match(pattern2, str(weight)):
            return weight
        else:
            return np.nan  
    
    @staticmethod
    def convert_to_kg(weight):
        '''
        This method converts different weight units to kilograms.

        Args:
         weight (str): A string representing the weight.

        Returns:
         float or NaN: The weight in kilograms or NaN if invalid.
         
        '''
        weight = str(weight)
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
                    quantity = float(quantity.strip())
                    value = float(value.replace(unit, '').strip()) #strip handles spaces
                    return quantity * value * conversion_factors[unit]
                else:
                    value = float(weight.replace(unit, '').strip()) 
                    return value * conversion_factors[unit]
             except ValueError:
                return np.nan

    def convert_product_weights(self, df, column_name):
        '''
        This method cleans and converts the weight column to float in kg.

        Args: 
         df (DataFrame): DataFrame containing products data

        Returns: 
         pd.DataFrame: DataFrame with cleaned weight column.

        '''
       
        df[column_name] = df['weight'].apply(DataCleaning.clean_weight) #is this appropriate? or self.clean_weight
        df[column_name] = df['weight'].apply(DataCleaning.convert_to_kg)

        return df
        
    def clean_products_data(self, products_data): 
        '''
        This method cleans the products data.

        Args: 
         products_data (pd.DataFrame): DataFrame containing products data. 
        Returns: 
         pd.DataFrame: DatFrame with cleaned products data.

        '''
        # products_data = pd.read_csv('products.csv') - redundant if already an argument 
        products_data['product_price'] = products_data['product_price'].str.replace(r'^(?!£).*$', '', regex=True) 
        products_data = self.covert_product_weights(products_data, 'weight')
        products_data = self.clean_null_and_empty(products_data)
        products_data = self.parse_dates(products_data, 'date_added')

        return products_data

    def clean_orders_data(self, orders_data):
        '''
        This method cleans the orders table data.

        Args: 
         orders_data (pd.DataFrame): DataFrame with the orders data. 

        Returns: 
         pd.DataFrame: DataFrame with cleaned orders data.

        '''
        orders_data = orders_data.drop(columns=['first_name', 'last_name', '1']) #drop these columns
        orders_data= self.clean_null_and_empty(orders_data)
    
        return orders_data      
    
    def clean_date_data(self, date_data):
        '''
        This method cleans the date_times table.

        Args: 
         date_data (pd.DataFrame): DataFrame with date times data.

        Returns: 
         pd.DataFrame: DataFrame with cleaned date data.

        '''
        date_data['year'] = date_data['year'].apply(lambda year: re.sub(r'^(?!\d{4}$).*', '', year))
        date_data = self.clean_null_and_empty(date_data)

        return date_data
    

    

       
       

