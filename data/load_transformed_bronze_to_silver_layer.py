import os
import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not connection_string:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "silver"
blob_name = "silver_civicpulse_data.parquet"

blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
)

# Load cleaned CSV

# FILE_NAME = "silver_civicpulse_data.csv"
# #df = pd.read_csv(FILE_NAME)

# print("Shape:", df.shape)
# print(df.head())

df = pd.read_csv("silver_civicpulse_data.csv")

# Convert to Parquet
df.to_parquet("silver_civicpulse_data.parquet", index=False)

# Upload correct file
with open("silver_civicpulse_data.parquet", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("Silver layer uploaded")