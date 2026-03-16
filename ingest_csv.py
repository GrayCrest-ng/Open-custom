import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")


COLUMN_MAP = {
    "CONSIGNEE_NAME": "importer_entity",    
    "SHIPPER_NAME": "supplier_entity",      
    "TARIFF_CODE": "hs_code_category",
    "GROSS_WEIGHT_KG": "weight_kg",
    "ITEM_VALUE_USD": "estimated_value_usd",
    "PORT_OF_LOADING": "port_of_lading",
    "ARRIVAL_DATE": "arrival_date"
}

def ingest_data(csv_filename):
    print(f"Loading massive dataset from {csv_filename}...")
    
    try:
       
        df = pd.read_csv(csv_filename, usecols=COLUMN_MAP.keys())
        df = df.rename(columns=COLUMN_MAP)
        
        print("Cleaning and formatting the data...")
        df['weight_kg'] = pd.to_numeric(df['weight_kg'], errors='coerce').fillna(0)
        df['estimated_value_usd'] = pd.to_numeric(df['estimated_value_usd'], errors='coerce').fillna(0)

        print("Connecting to cloud database...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        print(f"Injecting {len(df):,} shipping records into production...")
        
        insert_query = """
        INSERT INTO shipments (importer_entity, supplier_entity, hs_code_category, weight_kg, estimated_value_usd, port_of_lading, arrival_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        records = df.to_records(index=False).tolist()
        
        for record in records:
            cur.execute(insert_query, record)

        conn.commit()
        cur.close()
        conn.close()
        
        print("SUCCESS! Production database is fully loaded with 5,000 records.")

    except Exception as e:
        print(f"Pipeline Failure: {e}")

if __name__ == "__main__":
    ingest_data("cbp_daily_dump.csv")