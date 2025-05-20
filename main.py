import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "01 renewable-share-energy.csv"
TARGET_ENTITY = "World"

try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"File not found: {CSV_FILE}")
    exit(1)
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

required_columns = ["Entity", "Year", "Renewables (% equivalent primary energy)"]
if not all(col in df.columns for col in required_columns):
    print("CSV file missing required columns.")
    exit(1)

entity_data = df[df["Entity"] == TARGET_ENTITY]

if entity_data.empty:
    print(f"No data found for entity: {TARGET_ENTITY}")
    exit(1)

plt.figure(figsize=(10, 6))
plt.plot(entity_data["Year"], entity_data["Renewables (% equivalent primary energy)"], marker='o', linestyle='-')
plt.title(f"Renewable Energy Share Over Time - {TARGET_ENTITY}")
plt.xlabel("Year")
plt.ylabel("Renewables (% of primary energy)")
plt.grid(True)
plt.tight_layout()
plt.show()
