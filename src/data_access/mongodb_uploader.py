import os
import logging
from typing import List
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MongoUploader:
    def __init__(self, db_name: str, collection_name: str, connection_uri: str):
        self.db_name = db_name
        self.collection_name = collection_name
        self.connection_uri = connection_uri
        self.client = None
        self.collection = None

    def connect(self):
        """Connect to MongoDB instance."""
        try:
            self.client = MongoClient(self.connection_uri)
            self.client.admin.command("ping")  # Validate connection
            self.collection = self.client[self.db_name][self.collection_name]
            logging.info(f"Connected to MongoDB: {self.db_name}.{self.collection_name}")
        except ConnectionFailure as e:
            logging.error("MongoDB connection failed.")
            raise e

    def upload_csv(self, csv_path: str):
        """Upload CSV data to MongoDB."""
        try:
            df = pd.read_csv(csv_path)
            logging.info(f"Loaded CSV with shape {df.shape}")
            records = df.to_dict(orient="records")
            if records:
                result = self.collection.insert_many(records)
                logging.info(f"Inserted {len(result.inserted_ids)} records into MongoDB.")
            else:
                logging.warning("No records found to insert.")
        except BulkWriteError as bwe:
            logging.error("Bulk write failed.")
            raise bwe
        except Exception as e:
            logging.error("Error during CSV upload.")
            raise e

    def download_to_df(self) -> pd.DataFrame:
        """Retrieve data back from MongoDB into a DataFrame."""
        try:
            data = list(self.collection.find())
            df = pd.DataFrame(data).drop(columns=["_id"], errors="ignore")
            logging.info(f"Retrieved {len(df)} records from MongoDB.")
            return df
        except Exception as e:
            logging.error("Error retrieving data from MongoDB.")
            raise e

if __name__ == "__main__":
    # Load secrets from environment variables
    DB_NAME = os.getenv("MONGO_DB", "Project1")
    COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "Project1-Data")
    CONNECTION_URL = os.getenv("MONGO_URI")

    if not CONNECTION_URL:
        raise ValueError("MONGO_URI environment variable not set")

    uploader = MongoUploader(DB_NAME, COLLECTION_NAME, CONNECTION_URL)
    uploader.connect()
    uploader.upload_csv("C:\SUMMER LEARNING\PROJECTS\PROJECT\src\data_access\data.csv")
    df = uploader.download_to_df()
    print(df.head(2))
