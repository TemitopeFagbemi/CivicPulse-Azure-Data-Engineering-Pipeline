import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from azure.storage.blob import BlobServiceClient
from io import BytesIO

load_dotenv()

# -----------------------------
# LOAD FROM BLOB
# -----------------------------
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not connection_string:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "silver"
blob_name = "silver_civicpulse_data.parquet"

print("Downloading Silver data...")

data = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
).download_blob().readall()

df = pd.read_parquet(BytesIO(data))

print("Silver data loaded:", df.shape)

# -----------------------------
# GOLD TRANSFORMATION
# -----------------------------

gold_df = (
    df.groupby(["created_date_only", "status", "city_borough", "complaint_category"])
      .agg(
          complaint_count=("complaint_category", "count"),
          avg_latitude=("latitude", "mean"),
          avg_longitude=("longitude", "mean")
      )
      .reset_index()
)

# Rename for business clarity
gold_df = gold_df.rename(columns={
    "city_borough": "location",
    "complaint_category": "service_type"
})

# Add surrogate key
gold_df.insert(0, "summary_id", range(1, len(gold_df) + 1))

print("Gold data created:", gold_df.shape)
print(gold_df.head())

# -----------------------------
# LOAD TO POSTGRES
# -----------------------------
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require"
)

print("Uploading to PostgreSQL...")

gold_df.to_sql(
    "civicpulse_data_summary",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)

print("✅ Gold data loaded into PostgreSQL")