from sentence_transformers import SentenceTransformer
import json
import os


# -----------------------------
# Paths
# -----------------------------

INPUT_FILE = "data/processed/chunks.json"
OUTPUT_DIR = "data/processed/embeddings"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "embeddings.json"
)


# -----------------------------
# Create output directory
# -----------------------------

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# -----------------------------
# Load chunks
# -----------------------------

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)


print("Total chunks:", len(chunks))


# -----------------------------
# Load embedding model
# -----------------------------

print("\nLoading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# -----------------------------
# Extract text
# -----------------------------

texts = [
    chunk["text"]
    for chunk in chunks
]


# -----------------------------
# Generate embeddings
# -----------------------------

print("\nGenerating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)


print("Embedding shape:", embeddings.shape)


# -----------------------------
# Save embeddings
# -----------------------------

data = []

for chunk, embedding in zip(
    chunks,
    embeddings
):

    data.append({
        "chunk_id": chunk["chunk_id"],
        "source": chunk["source"],
        "title": chunk["title"],
        "file": chunk["file"],
        "text": chunk["text"],
        "embedding": embedding.tolist()
    })


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f
    )


print("\n------------------------------")
print("Embedding completed!")
print("Total embeddings:", len(data))
print("Saved:", OUTPUT_FILE)
print("------------------------------")