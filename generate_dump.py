import pandas as pd
import random
from datetime import datetime, timedelta


importers = ["Yeti Coolers LLC", "YETI CUSTOM DOMESTIC", "Apple Inc.", "APPLE OPERATIONS INTL", "Nike Inc.", "NIKE USA", "Samsung Electronics", "Tesla Motors"]
suppliers = ["Shenzhen Plastics Co", "Foxconn Technology", "Pou Chen Corp", "BYD Auto", "Vietnam Manuf Group", "TSMC", "LG Chem"]
ports = ["Shenzhen", "Los Angeles", "Ho Chi Minh", "Long Beach", "Rotterdam", "Shanghai"]
hs_codes = ["3923.10", "8517.12", "6404.11", "8703.80", "8542.31"]

print("Generating simulated CBP daily dump (5,000 records)...")

data = []
for i in range(5000):
    data.append({
        "CONSIGNEE_NAME": random.choice(importers) + " " + random.choice(["", "CORP", "INC", "LTD"]), # Adding noise
        "SHIPPER_NAME": random.choice(suppliers),
        "TARIFF_CODE": random.choice(hs_codes),
        "GROSS_WEIGHT_KG": round(random.uniform(1000, 50000), 2),
        "ITEM_VALUE_USD": round(random.uniform(10000, 2000000), 2),
        "PORT_OF_LOADING": random.choice(ports),
        "ARRIVAL_DATE": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
    })


df = pd.DataFrame(data)
df.to_csv("cbp_daily_dump.csv", index=False)
print("Success! Created 'cbp_daily_dump.csv' with 5,000 records.")