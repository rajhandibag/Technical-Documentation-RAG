import requests
from bs4 import BeautifulSoup
import os
import shutil
import json


input_file = "data/raw/urls.txt"
output_folder = "data/raw/pages"
raw_metadata_file = "data/raw/metadata_raw.json"

# --------------------------------
# Clear stale files
# --------------------------------
if os.path.exists(output_folder):
    print("Clearing output folder:", output_folder)
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
else:
    os.makedirs(output_folder, exist_ok=True)

if os.path.exists(raw_metadata_file):
    try:
        os.unlink(raw_metadata_file)
    except Exception as e:
        print(f"Failed to delete {raw_metadata_file}. Reason: {e}")

# --------------------------------
# Read URLs
# --------------------------------

with open(input_file, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

metadata_raw = []

# --------------------------------
# Scrape every URL
# --------------------------------

for i, url in enumerate(urls, start=1):

    print(f"\nScraping {i}/{len(urls)}")
    print(url)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        print("Status:", response.status_code)
        print("Actual URL:", response.url)

        if response.status_code != 200:
            print("Failed")
            continue

        # Check if redirect happened
        if response.url != url:
            print(f"Warning: Redirected from {url} to {response.url}")

        # --------------------------------
        # Force UTF-8
        # --------------------------------

        response.encoding = "utf-8"

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Get page title
        title = "No Title"
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        print("Title:", title)

        # --------------------------------
        # Find main document
        # --------------------------------

        document = soup.find(
            "div",
            class_="document"
        )

        if not document:
            print("Document not found")
            continue

        # --------------------------------
        # Find documentwrapper
        # --------------------------------

        documentwrapper = document.find(
            "div",
            class_="documentwrapper"
        )

        if not documentwrapper:
            print("Document wrapper not found")
            continue

        # --------------------------------
        # Find bodywrapper
        # --------------------------------

        bodywrapper = documentwrapper.find(
            "div",
            class_="bodywrapper"
        )

        if not bodywrapper:
            print("Body wrapper not found")
            continue

        # --------------------------------
        # Find actual documentation body
        # --------------------------------

        body = bodywrapper.find(
            "div",
            class_="body"
        )

        if not body:
            print("Main body not found")
            continue

        # --------------------------------
        # Extract text
        # --------------------------------

        text = body.get_text(
            "\n",
             strip=True
        )

        title = soup.title.get_text(strip=True) if soup.title else ""

        text = (
            f"Source: {url}\n"
            f"Title: {title}\n\n"
            f"{text}"
        )

        # --------------------------------
        # Save
        # --------------------------------

        file_name = f"page_{i}.txt"
        file_path = os.path.join(
            output_folder,
            file_name
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

        print("Saved:", file_path)
        print("Characters:", len(text))

        # Add to metadata_raw
        metadata_raw.append({
            "id": i,
            "file": file_name,
            "requested_url": url,
            "actual_url": response.url,
            "title": title
        })

    except requests.RequestException as e:

        print("Request error:", e)


# --------------------------------
# Save raw metadata
# --------------------------------
with open(raw_metadata_file, "w", encoding="utf-8") as f:
    json.dump(
        metadata_raw,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\nScraping completed successfully! Raw metadata saved for {len(metadata_raw)} pages.")