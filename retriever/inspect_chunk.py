import json


INPUT_FILE = "data/processed/chunks.json"


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)


print("Total chunks:", len(chunks))


for i, chunk in enumerate(chunks[:5], start=1):

    print("\n" + "=" * 80)

    print("Chunk:", i)
    print("Chunk ID:", chunk["chunk_id"])
    print("File:", chunk["file"])

    print("\nTEXT:")
    print(chunk["text"])