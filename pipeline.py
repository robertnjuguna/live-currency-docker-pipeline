import pandas as pd
import requests
import os
from sqlalchemy import create_engine
import time

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

print("Starting the Live currency pipeleine....")
print("waiting for 15 sec for the finace database network to stabilize...")
time.sleep(15)

#1. fetching data from a free online API
print("reaching out the internet to get live exchange rates...")

url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url)
data = response.json()

# 2. Extracting and transforming data using pandas
rates = data["rates"]

# picking a few currecies to track
tracked_currencies = {
    "Currency": ["Kenya Shilling (KES)", "Euro (EUR)", "British Pound (GBP)", "Japanese Yen (JPY)"],
    "Rates_per_1_USD": [rates.get("KES"), rates.get("EUR"), rates.get("GBP"), rates.get("JPY")]
}

df = pd.DataFrame(tracked_currencies)
df["last_updated"] = pd.to_datetime("now")

print("Cleaned Data Snapshot:")
print(df)

#3. Connecting to our Docker Compose Postgres Servise

DB_URL = f"postgresql://{db_user}:{db_password}@currency-db:5432/{db_name}"
engine = create_engine(DB_URL)

print("Loding market exchange rates data into Postgres Container...")
#4. Loading the data into the database
df.to_sql("exchange_rate", engine, if_exists="replace", index = False)

print("Data loaded into a postgres Container!")
