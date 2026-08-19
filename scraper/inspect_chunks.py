import json

file_path = "data/processed/chunks.json"

with open(file_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Total chunks:", len(chunks))

print("\n" + "=" * 80)

for chunk in chunks[:5]:

    print("\nChunk ID:", chunk["chunk_id"])
    print("Source:", chunk["source"])
    print("Title:", chunk.get("title", "No Title"))
    print("File:", chunk["file"])
    print("\nTEXT:")
    print(chunk["text"])

    print("\n" + "=" * 80)