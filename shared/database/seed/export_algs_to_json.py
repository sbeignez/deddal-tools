import os
import json
import requests
import pandas as pd
from io import StringIO

# Get the base sheet ID from environment
SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
if not SHEET_ID:
    raise Exception("Missing GOOGLE_SHEET_ID environment variable.")

# Tabs to export
TABS = ["Algorithms", "Cases", "Pattern"]

# Base URL template
CSV_URL_TEMPLATE = "https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Output directory
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for tab in TABS:
    print(f"Processing tab: {tab}")
    csv_url = CSV_URL_TEMPLATE.format(sheet_id=SHEET_ID, sheet_name=tab)

    # Fetch CSV and read into pandas directly
    response = requests.get(csv_url)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))

    # Optional: Add version metadata here
    json_data = df.to_dict(orient='records')

    # Save JSON
    filename = f"{tab.lower().replace(' ', '_')}.json"
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(output_path, "w") as json_file:
        json.dump(json_data, json_file, indent=2)

    print(f"✅ Saved {output_path}")
