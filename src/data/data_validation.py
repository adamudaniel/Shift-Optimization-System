import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
import sys

from src.logger import configure_logger
from src.exception import CustomException as MyException
from src.data.data_ingestion import load_data

logging = configure_logger()

class DataValidation:
    """
    A class to perform checks and data validation on the Shift Performance data.
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data
        logging.info("DataValidation class initialized.")

    def check_data_if_empty(self):
        """
        Check for null values in the data and raise an exception if empty.
        """
        try:
            logging.info("Checking if data table is empty...")
            if self.data.empty:
                raise ValueError("The ingested DataFrame contains zero records.")
            else:
                logging.info("Data is not empty.")
        except Exception as e:
            logging.error(f"Error checking if data is empty: {e}")
            raise MyException(e, sys)
        
    def checking_missing_values(self):
        """
        Check for missing values in non-nullable operational columns.
        """
        try:
            logging.info("Checking critical columns for missing values...")
            
            # Define critical columns that must NEVER be missing (NaN)
            critical_columns = [
                'shift_id', 'shift_name', 'start_time', 'end_time', 
                'supervisor_id', 'production_id', 'date', 'units_produced', 
                'operator_id', 'machine_id', 'runtime_hours'
            ]
            
            # Check only our critical list
            missing_values = self.data[critical_columns].isnull().sum()
            
            if missing_values.sum() > 0:
                logging.warning(f"Critical missing values found:\n{missing_values[missing_values > 0]}")
                raise ValueError(f"Critical missing values found in mandatory columns:\n{missing_values[missing_values > 0]}")
            else:
                logging.info("No critical missing values found. Optional maintenance gaps accepted.")
                
            return missing_values
            
        except Exception as e:
            # Wrapping it in a try-except gives 'sys' an active traceback context to read!
            logging.error(f"Missing values validation failed: {e}")
            raise MyException(e, sys)
    
    def checking_for_duplicates(self):
        """
        Check for duplicates in the data and log warnings if found.
        """
        try:
            duplicates = self.data.duplicated().sum()
            if duplicates > 0:
                logging.warning(f"Duplicates found in the data: {duplicates}")
            else:
                logging.info("No duplicates found in the data.")
        except Exception as e:
            logging.error(f"Error checking for duplicates: {e}") 
            raise MyException(e, sys)
        
def starting_datavalidation(data: pd.DataFrame):
    """
    Start the data validation process by performing all checks.
    """
    try:
        logging.info("Starting data validation process...")
        validator_engine = DataValidation(data)
        validator_engine.check_data_if_empty()
        validator_engine.checking_missing_values()
        validator_engine.checking_for_duplicates()

        logging.info("Data validation process completed successfully.")
        return data

    except Exception as e:
        logging.error(f"Error during data validation suite execution: {e}")
        raise MyException(e, sys)
        
if __name__ == "__main__":
    data = load_data()
    starting_datavalidation(data)