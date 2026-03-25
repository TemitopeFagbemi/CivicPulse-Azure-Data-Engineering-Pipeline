import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from azure.storage.blob import BlobServiceClient

load_dotenv()

# Load Azure connection string
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not connection_string:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")

# Connect to Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "silver"
blob_name = "silver_civicpulse_data.parquet"

blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
)

# Base folder of this script
BASE_DIR = Path(__file__).resolve().parent

# File paths
csv_path = BASE_DIR / "silver_civicpulse_data.csv"
parquet_path = BASE_DIR / "silver_civicpulse_data.parquet"

# Load cleaned CSV
df = pd.read_csv(csv_path)

print("Shape:", df.shape)
print(df.head())

# Convert CSV to Parquet
df.to_parquet(parquet_path, index=False)

# Upload Parquet to Azure Blob
with open(parquet_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("Silver layer uploaded successfully")