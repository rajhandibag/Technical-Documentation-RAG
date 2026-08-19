import os
import re
import shutil

input_folder = "data/raw/pages"
output_folder = "data/cleaned"

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


def clean_text(text):

    # --------------------------------
    # 1. Normalize line endings
    # --------------------------------
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # --------------------------------
    # 2. Remove very common page noise
    # --------------------------------
    noise_patterns = [
        r"^Previous topic$",
        r"^Next topic$",
        r"^This Page$",
        r"^Report a Bug$",
        r"^Show Source$",
        r"^Navigation$",
        r"^Table of Contents$",
    ]

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            cleaned_lines.append("")
            continue
        if line == "¶":
            continue
        # Remove visual navigation artifacts
        if line in ["_", "|", "«", "»", "¶"]:
            continue

        # Remove known noise
        remove_line = False

        for pattern in noise_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                remove_line = True
                break

        if not remove_line:
            cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # --------------------------------
    # 3. Remove excessive blank lines
    # --------------------------------
    text = re.sub(r"\n{3,}", "\n\n", text)

    # --------------------------------
    # 4. Remove excessive spaces
    # --------------------------------
    text = re.sub(r"[ \t]+", " ", text)

    # --------------------------------
    # 5. Remove spaces before punctuation
    # --------------------------------
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    # --------------------------------
    # 6. Remove repeated separators
    # --------------------------------
    text = re.sub(r"[-_=]{5,}", "", text)

    # --------------------------------
    # 7. Final cleanup
    # --------------------------------
    text = text.strip()

    return text


# --------------------------------
# Process all files
# --------------------------------

for filename in os.listdir(input_folder):

    if not filename.endswith(".txt"):
        continue

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    cleaned_text = clean_text(text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print("Cleaned:", filename)

print("\nCleaning completed successfully!")