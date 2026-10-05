import sys
import os
import json
import faiss

from sentence_transformers import SentenceTransformer

# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from generator.generate_answer import generate_answer


# --------------------------------
# Paths
# --------------------------------

INDEX_FILE = "data/processed/faiss/index.faiss"
METADATA_FILE = "data/processed/faiss/metadata.json"


# --------------------------------
# Load FAISS index
# --------------------------------

index = faiss.read_index(INDEX_FILE)

print("FAISS index loaded")
print("Total vectors:", index.ntotal)


# --------------------------------
# Load metadata
# --------------------------------

with open(
    METADATA_FILE,
    "r",
    encoding="utf-8"
) as f:

    metadata = json.load(f)


# --------------------------------
# Load embedding model
# --------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------
# Search function
# --------------------------------

def search(query, top_k=3):

    # Convert query into embedding
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = query_embedding.astype(
        "float32"
    )

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    # Store retrieved documents
    retrieved_docs = []

    print("\n" + "=" * 80)
    print("RETRIEVED DOCUMENTS")
    print("=" * 80)

    for rank, (distance, idx) in enumerate(
        zip(distances[0], indices[0]),
        start=1
    ):

        result = metadata[idx]

        print(f"\nResult {rank}")
        print("-" * 80)

        print("Distance:", distance)
        print("Title:", result["title"])
        print("Source:", result["source"])

        # Store complete information
        retrieved_docs.append({
            "title": result["title"],
            "source": result["source"],
            "text": result["text"],
            "distance": float(distance)
        })

    return retrieved_docs


# --------------------------------
# Main RAG pipeline
# --------------------------------

if __name__ == "__main__":

    question = input(
        "\nEnter your question: "
    )

    # Retrieve relevant documents
    documents = search(
        question,
        top_k=3
    )

    # Generate answer using retrieved context
    answer = generate_answer(
        question,
        documents
    )

    print("\n" + "=" * 80)
    print("FINAL ANSWER")
    print("=" * 80)

    print(answer)