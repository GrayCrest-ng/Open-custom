import os
import psycopg2
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
db_url = os.getenv("DATABASE_URL")
port = int(os.environ.get("PORT", 8000))

mcp = FastMCP("OpenCustoms", host="0.0.0.0", port=port)


class ShipmentRecord(BaseModel):
    importer_entity: str
    supplier_entity: str
    hs_code_category: str
    weight_kg: float
    estimated_value_usd: float
    port_of_lading: str
    arrival_date: str

@mcp.tool()
def get_raw_shipment_data(company_name: str) -> List[ShipmentRecord]:
    """
    Returns normalized, raw Bill of Lading JSON data for a specific company.
    Uses fuzzy matching to find the closest company name.
    """
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        query = """
            SELECT importer_entity, supplier_entity, hs_code_category, weight_kg, estimated_value_usd, port_of_lading, arrival_date 
            FROM shipments 
            ORDER BY importer_entity <-> %s 
            LIMIT 5;
        """
        
        cur.execute(query, (company_name,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        results = []
        for row in rows:
            
            results.append(ShipmentRecord(
                importer_entity=str(row[0]),
                supplier_entity=str(row[1]),
                hs_code_category=str(row[2]),
                weight_kg=float(row[3]) if row[3] else 0.0, 
                estimated_value_usd=float(row[4]) if row[4] else 0.0,
                port_of_lading=str(row[5]),
                arrival_date=str(row[6]) 
            ))
        
        return results

    except Exception as e:
        raise RuntimeError(f"Database error: {str(e)}")


@mcp.tool()
def analyze_supply_chain(company_name: str) -> str:
    """
    Acts as a supply chain analyst. Returns a human-readable intelligence report 
    on a competitor's manufacturers, total shipment volume, and estimated value.
    """
    try:
        shipments = get_raw_shipment_data(company_name)
        
        if not shipments:
            return f"No supply chain data found for {company_name}."

        
        total_weight = sum(s.weight_kg for s in shipments)
        total_value = sum(s.estimated_value_usd for s in shipments)
        
        suppliers = [s.supplier_entity for s in shipments]
        top_supplier = max(set(suppliers), key=suppliers.count) if suppliers else "Unknown"
        
        report = (
            f"SUPPLY CHAIN INTELLIGENCE REPORT: {company_name.upper()} 🎯\n\n"
            f"Primary Manufacturer: {top_supplier}\n"
            f"Total Shipments Tracked: {len(shipments)}\n"
            f"Total Container Weight: {total_weight:,.2f} kg\n"
            f"Estimated Import Value: ${total_value:,.2f} USD\n\n"
            f"Analysis: {company_name.upper()} relies heavily on {top_supplier} for its manufacturing. "
            f"Agent, you can use the 'get_raw_shipment_data' tool if you need the exact arrival dates and port locations."
        )
        
        return report

    except Exception as e:
        return f"Error analyzing supply chain: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse")