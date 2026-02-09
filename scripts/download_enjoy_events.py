import requests
import pandas as pd
import os

URL = "https://enjoy.sa/api/v1/odp/events/Get"

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://enjoy.sa",
    "Origin": "https://enjoy.sa"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

data = response.json()

if isinstance(data, list):
    df = pd.DataFrame(data)
else:
    df = pd.DataFrame(data.get("data", []))

out_dir = "data/raw/open_data_events"
os.makedirs(out_dir, exist_ok=True)

output_path = f"{out_dir}/enjoy_events_raw.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("✅ Enjoy Events downloaded successfully")
print("📁 Saved to:", output_path)
print("📊 Rows:", df.shape[0], "| Columns:", df.shape[1])
