import pandas as pd

url = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=1000"

df = pd.read_csv(url)

df.to_csv("civicpulse_data.csv", index=False)

print(df.head())