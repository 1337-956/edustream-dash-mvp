import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text

# =====================================================================
# POSTGRESQL CONNECTION CONFIGURATION
# =====================================================================
# TODO: Update 'postgres' and 'password' if you use different local credentials
DB_USER = "postgres"
DB_PASS = "password" 
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "edustream_db"

# Connect to default database first to programmatically ensure edustream_db exists
base_engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres")
with base_engine.connect() as conn:
    conn.execute(text("COMMIT;"))
    db_check = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")).fetchone()
    if not db_check:
        conn.execute(text(f"CREATE DATABASE {DB_NAME};"))
        print(f"Database '{DB_NAME}' created successfully.")

# Initialize production engine connection
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("Starting ETL Ingestion Layer...")
try:
    # Query the Hipo Labs API endpoint from your project scope
    url = "http://universities.hipolabs.com/search?country=United+States"
    response = requests.get(url)
    if response.status_code == 200:
        raw_data = response.json()
        print(f"Extracted {len(raw_data)} raw records from Hipo Labs REST API.")
    else:
        raise Exception(f"API Connection Failed: {response.status_code}")

    # Transformation & Flattening Layer
    df_raw = pd.DataFrame(raw_data)
    df_clean = pd.DataFrame({
        'university_name': df_raw['name'].str.strip(),
        'state_province': df_raw['state-province'].fillna('Not Specified').str.strip(),
        'country_name': df_raw['country'].str.strip(),
        'alpha_two_code': df_raw['alpha_two_code'].str.strip()
    })
    
    # Strip away empty rows to keep charts clean
    df_clean = df_clean[(df_clean['state_province'] != 'Not Specified') & (df_clean['state_province'] != '')]

    print("Loading structured data into PostgreSQL target table...")
    df_clean.to_sql('fact_universities', con=engine, if_exists='replace', index=False)
    
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM fact_universities")).fetchone()
        print(f"Success! Programmatically verified {count} production rows in PostgreSQL.")

except Exception as e:
    print(f"[CRITICAL ERROR] Ingestion script halted: {e}")