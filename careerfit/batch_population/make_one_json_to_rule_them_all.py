import json
from careerfit.globals import COMPANIES_DIR, COMPANIES_FILE


merged_data = []

for json_file in COMPANIES_DIR.glob("*.json"):
    try:
        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                merged_data.extend(data)
            else:
                merged_data.append(data)
    except json.JSONDecodeError:
        print(f"Skipping invalid JSON file: {json_file}")

with COMPANIES_FILE.open("w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=4)

print(f"Merged JSON data saved to {COMPANIES_FILE}")
