import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()
db_url = os.getenv("DATABASE_URL")

def seed_database():
    try:
        print("Connecting to Neon database...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        
        mock_shipments = [
            ('Yeti Coolers LLC', 'Shenzhen Plastics Co', '3923.10', 4500, 120000, 'Shenzhen', '2026-01-15'),
            ('YETI CUSTOM DOMESTIC', 'Shenzhen Plastics Co', '3923.10', 5200, 135000, 'Shenzhen', '2026-02-10'),
            ('Yeti Coolers', 'Vietnam Manuf Group', '3923.10', 2100, 60000, 'Ho Chi Minh', '2026-03-01'),
            ('Nike Inc', 'Pou Chen Corp', '6404.11', 12000, 500000, 'Taiwan', '2026-02-28'),
            ('Apple Operations Intl', 'Foxconn Technology Group', '8517.12', 8500, 2500000, 'Shenzhen', '2026-03-05')
        ]

        print("Inserting fake supply chain data...")
        
        
        insert_query = """
        INSERT INTO shipments (importer_entity, supplier_entity, hs_code_category, weight_kg, estimated_value_usd, port_of_lading, arrival_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        
        for shipment in mock_shipments:
            cur.execute(insert_query, shipment)

        
        conn.commit()
        cur.close()
        conn.close()
        print("Success! The warehouse is fully stocked with mock data.")

    except Exception as e:
        print(f"Uh oh, something went wrong: {e}")

if __name__ == "__main__":
    seed_database()