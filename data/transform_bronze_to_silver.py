import pandas as pd
from pathlib import Path

# Bronze file
bronze_path = Path("bronze_civicpulse_data.csv")

# Read raw data
df = pd.read_csv(bronze_path)

print("Raw rows:", len(df))
print(df.columns)

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Rename columns early
df = df.rename(columns={
    "created_date_only": "created_date",
    "complaint_type": "complaint_category",
    "borough": "city_borough",
    "open_data_channel_type": "submission_method"
})

# Convert datetime
df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")


# Split into date + time
df["created_date_only"] = df["created_date"].dt.date
df["created_time_only"] = df["created_date"].dt.time
df["closed_date_only"] = df["closed_date"].dt.date
df["closed_time_only"] = df["closed_date"].dt.time

# Drop original datetime
df.drop(columns=["created_date", "closed_date"], inplace=True)

# Remove duplicates
df = df.drop_duplicates()

# Remove rows with missing important fields
df = df.dropna(subset=["complaint_category", "city_borough", "latitude", "longitude"])

# Convert coordinates to numeric
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

# Remove rows with missing coordinates
df = df.dropna(subset=["latitude", "longitude"])

# Filter valid NYC coordinates
df = df[
    (df["latitude"].between(40.4, 41.0)) &
    (df["longitude"].between(-74.3, -73.6))
]

print("Rows after cleaning:", len(df))

# Select final columns
columns = [
    "created_date_only",
    "created_time_only",
    "closed_date_only",
    "closed_time_only",
    "complaint_category",
    "city_borough",
    "latitude",
    "longitude",
    "agency_name",
    "descriptor",
    "status",
    "resolution_description",
    "resolution_action_updated_date",
    "park_borough",
    "submission_method"
]

df_silver = df[columns]

# Save Silver dataset
silver_path = Path("silver_civicpulse_data.csv")
df_silver.to_csv(silver_path, index=False)

print("Silver dataset created:", silver_path)
print("Clean rows:", len(df_silver))