import json
import os

raw_metadata_file = "data/raw/metadata_raw.json"
cleaned_folder = "data/cleaned"
output_file = "data/processed/metadata.json"

os.makedirs("data/processed", exist_ok=True)

if not os.path.exists(raw_metadata_file):
    print(f"Error: Raw metadata file {raw_metadata_file} not found. Run scraper first.")
    exit(1)

# Read raw metadata
with open(raw_metadata_file, "r", encoding="utf-8") as f:
    metadata_raw = json.load(f)

metadata = []

for entry in metadata_raw:

    filename = entry["file"]
    filepath = os.path.join(cleaned_folder, filename)

    # Skip if cleaned file doesn't exist
    if not os.path.exists(filepath):
        print("Missing cleaned file for:", filename)
        continue

    metadata.append({
        "id": entry["id"],
        "file": filename,
        "source": entry["actual_url"],
        "title": entry["title"]
    })

# Save metadata
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        metadata,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\nMetadata created for {len(metadata)} documents.")
print("Saved:", output_file)