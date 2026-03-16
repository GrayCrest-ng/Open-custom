import os
import psycopg2
from dotenv import load_dotenv

# 1. Load the secret connection string from your .env file
load_dotenv()
db_url = os.getenv("DATABASE_URL")

def setup_database():
    try:
        # 2. Connect to the Neon PostgreSQL database
        print("Connecting to Neon database...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # 3. Turn on the fuzzy matching extension (This is our technical moat!)
        print("Enabling pg_trgm extension...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

        # 4. Create the shipments table with our normalized schema
        print("Creating the shipments table...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS shipments (
            id SERIAL PRIMARY KEY,
            importer_entity VARCHAR(255),
            supplier_entity VARCHAR(255),
            hs_code_category VARCHAR(100),
            weight_kg NUMERIC,
            estimated_value_usd NUMERIC,
            port_of_lading VARCHAR(255),
            arrival_date DATE
        );
        """
        cur.execute(create_table_query)

        # 5. Build the high-speed search indexes for the AI
        print("Building search indexes...")
        index_query = """
        CREATE INDEX IF NOT EXISTS trgm_idx_importer ON shipments USING gin (importer_entity gin_trgm_ops);
        CREATE INDEX IF NOT EXISTS trgm_idx_supplier ON shipments USING gin (supplier_entity gin_trgm_ops);
        """
        cur.execute(index_query)

        # Save our changes and close the door
        conn.commit()
        cur.close()
        conn.close()
        print("Success! The OpenCustoms database is fully prepped and ready.")

    except Exception as e:
        print(f"Uh oh, something went wrong: {e}")

if __name__ == "__main__":
    setup_database()