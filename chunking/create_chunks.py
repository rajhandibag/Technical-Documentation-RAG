import os
import json
import re

INPUT_FOLDER = "data/raw/pages"
OUTPUT_FILE = "data/processed/chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def extract_metadata(text):
    """
    Extract Source and Title from the scraped page.
    """

    source = ""
    title = ""

    source_match = re.search(
        r"Source:\s*(.+)",
        text
    )

    title_match = re.search(
        r"Title:\s*(.+)",
        text
    )

    if source_match:
        source = source_match.group(1).strip()

    if title_match:
        title = title_match.group(1).strip()

    return source, title


def clean_text(text):
    """
    Remove metadata lines from actual document text.
    """

    text = re.sub(
        r"Source:\s*.+\n?",
        "",
        text
    )

    text = re.sub(
        r"Title:\s*.+\n?",
        "",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def create_chunks(text, chunk_size, overlap):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def main():

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    all_chunks = []

    files = sorted(
        [
            file
            for file in os.listdir(INPUT_FOLDER)
            if file.endswith(".txt")
        ]
    )

    for file_name in files:

        file_path = os.path.join(
            INPUT_FOLDER,
            file_name
        )

        print("Processing:", file_name)

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        # Extract metadata
        source, title = extract_metadata(text)

        # Remove metadata from document text
        text = clean_text(text)

        # Create chunks
        chunks = create_chunks(
            text,
            CHUNK_SIZE,
            CHUNK_OVERLAP
        )

        # Store chunks
        for i, chunk in enumerate(chunks):

            all_chunks.append({

                "chunk_id": f"{file_name}_{i}",

                "source": source,

                "title": title,

                "file": file_name,

                "text": chunk
            })

    # Save
    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\n------------------------------")
    print("Chunking completed!")
    print("Total chunks:", len(all_chunks))
    print("Saved:", OUTPUT_FILE)
    print("------------------------------")


if __name__ == "__main__":
    main()