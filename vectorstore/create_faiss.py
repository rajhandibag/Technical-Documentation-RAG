import json
import os
import numpy as np
import faiss


# --------------------------------
# Paths
# --------------------------------

INPUT_FILE = "data/processed/embeddings/embeddings.json"
OUTPUT_DIR = "data/processed/faiss"

INDEX_FILE = os.path.join(
    OUTPUT_DIR,
    "index.faiss"
)

METADATA_FILE = os.path.join(
    OUTPUT_DIR,
    "metadata.json"
)


# --------------------------------
# Create output directory
# --------------------------------

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# --------------------------------
# Load embeddings
# --------------------------------

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)


print("Total embeddings:", len(data))


# --------------------------------
# Convert embeddings to NumPy
# --------------------------------

embeddings = np.array(
    [item["embedding"] for item in data],
    dtype="float32"
)

print("Embedding shape:", embeddings.shape)


# --------------------------------
# Create FAISS index
# --------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)


# --------------------------------
# Add embeddings
# --------------------------------

index.add(embeddings)

print("Vectors stored in FAISS:", index.ntotal)


# --------------------------------
# Save FAISS index
# --------------------------------

faiss.write_index(
    index,
    INDEX_FILE
)


# --------------------------------
# Save metadata
# --------------------------------

metadata = []

for item in data:

    metadata.append({
        "chunk_id": item["chunk_id"],
        "source": item["source"],
        "title": item["title"],
        "file": item["file"],
        "text": item["text"]
    })


with open(
    METADATA_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metadata,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\n------------------------------")
print("FAISS index created!")
print("Dimension:", dimension)
print("Total vectors:", index.ntotal)
print("Index:", INDEX_FILE)
print("Metadata:", METADATA_FILE)
print("------------------------------")