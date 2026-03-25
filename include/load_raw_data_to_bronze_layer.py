import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()


connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not connection_string:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set")


blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client("bronze")
blob_client = container_client.get_blob_client("bronze_civicpulse_data.csv")

with open("bronze_civicpulse_data.csv", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("Upload complete")