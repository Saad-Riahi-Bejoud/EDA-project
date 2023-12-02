# db_utils.py
import yaml
from sqlalchemy import create_engine
import pandas as pd

class RDSDatabaseConnector:
    def __init__(self, credentials):
        self.credentials = credentials
        self.engine = self.create_engine()

    def create_engine(self):
        connection_str = f"postgresql+psycopg2://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
        engine = create_engine(connection_str)
        return engine

    def extract_data(self):
        query = "SELECT * FROM loan_payments"  # Customize the query based on your database schema
        data = pd.read_sql_query(query, self.engine)
        return data

    def save_data_local(self, data_frame, file_path):
        data_frame.to_csv(file_path, index=False)

def load_credentials(file_path='credentials.yaml'):
    with open(file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

if __name__ == "__main__":
    # Load credentials from the YAML file
    credentials = load_credentials()

    # Create an instance of RDSDatabaseConnector
    db_connector = RDSDatabaseConnector(credentials)

    # Extract data from the RDS database
    data = db_connector.extract_data()

    # Save the extracted data locally in CSV format
    db_connector.save_data_local(data, 'loan_payments_data.csv')
    

    print("Script executed successfully!")