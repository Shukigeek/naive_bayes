import pandas as pd
import requests
from sqlalchemy import create_engine
import logging


class DataLoader:
    def __init__(self):
        self.df = None
        logging.info("DataLoader initialized.")

    def load_data(self, path):
        logging.info(f"Attempting to load data from file: {path}")
        try:
            file_type = path.split('.')[-1]
            if file_type == "csv":
                self.df = pd.read_csv(path)

            elif file_type == "excel":
                self.df = pd.read_excel(path)
            elif file_type == "json":
                self.df = pd.read_json(path)
            else:
                raise ValueError("Unsupported file type.")
            logging.info(f"Data loaded successfully from {file_type.upper()} file: {path}")
        except FileNotFoundError:
            logging.error(f"File not found: {path}")
            self.df = None
        except ValueError as ve:
            logging.error(f"Value error while loading data: {ve}")
            self.df = None
        except Exception as e:
            logging.exception(f"Unexpected error while loading data: {e}")
            self.df = None

    def load_from_api(self, url):
        logging.info(f"Attempting to load data from API: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                self.df = pd.DataFrame(data)
            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        self.df = pd.DataFrame(value)
                        break
            else:
                raise ValueError("Unsupported JSON format.")
            logging.info("Data loaded successfully from API.")
        except Exception as e:
            logging.exception(f"Failed to load data from API: {e}")
            self.df = None

    def load_from_mysql(self, user, password, host, database, query):
        logging.info(f"Attempting to load data from MySQL: {host}/{database}")
        try:
            engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
            self.df = pd.read_sql_query(query, engine)
            logging.info("Data loaded successfully from MySQL.")
        except Exception as e:
            logging.exception(f"Failed to load data from MySQL: {e}")
            self.df = None

