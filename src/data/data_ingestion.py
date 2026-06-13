import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

from config.constant import database_path
from src.logger import configure_logger

logger = configure_logger()

def load_data():
    """
    Load data from the SQLite database and return it as a pandas DataFrame.
    """
    try:
        logger.info("Data ingestion started...")
        logger.info("Loading data from database....")
        # initialize the database connection
        connection = sqlite3.connect(database_path)
        # load data from the database into a pandas DataFrame
        Shift_Data = pd.read_sql("SELECT * FROM ShiftPerformance", connection)
        
        logger.info(Shift_Data.head())
        logger.info("Data ingestion completed successfully.")

        return Shift_Data
    except Exception as e:
        logger.error(f"Error loading data from database: {e}")
        raise MyException(e, sys)
    

load_data()