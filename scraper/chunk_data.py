import json
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------
# Paths
# --------------------------------

cleaned_folder = "data/cleaned"
metadata_file = "data/processed/metadata.json"
output_file = "data/processed/chunks.json"

# Clear stale output file
if os.path.exists(output_file):
    try:
        print("Removing stale chunks file:", output_file)
        os.unlink(output_file)
    except Exception as e:
        print(f"Failed to delete {output_file}. Reason: {e}")


# --------------------------------
# Load metadata
# --------------------------------

with open(metadata_file, "r", encoding="utf-8") as f:
    metadata = json.load(f)


# --------------------------------
# Create text splitter
# --------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


# --------------------------------
# Create chunks
# --------------------------------

all_chunks = []

for document in metadata:

    file_name = document["file"]
    source = document["source"]
    document_id = document["id"]
    title = document.get("title", "No Title")

    file_path = os.path.join(
        cleaned_folder,
        file_name
    )

    if not os.path.exists(file_path):
        print("Missing:", file_name)
        continue

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        text = f.read()

    chunks = text_splitter.split_text(text)

    print(
        f"{file_name}: {len(chunks)} chunks"
    )

    for chunk_id, chunk in enumerate(chunks):

        all_chunks.append({
            "chunk_id": f"{document_id}_{chunk_id}",
            "document_id": document_id,
            "source": source,
            "title": title,
            "file": file_name,
            "text": chunk
        })


# --------------------------------
# Save chunks
# --------------------------------

os.makedirs(
    "data/processed",
    exist_ok=True
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        indent=4,
        ensure_ascii=False
    )


print("\n------------------------------")
print("Chunking completed!")
print("Total chunks:", len(all_chunks))
print("Saved:", output_file)
print("------------------------------")