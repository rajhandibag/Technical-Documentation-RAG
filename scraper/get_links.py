import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://docs.python.org/3/"

response = requests.get(url)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

links = []

for a in soup.find_all("a", href=True):

    href = a["href"]

    full_url = urljoin(url, href)

    if full_url.startswith("https://docs.python.org/3/"):
        links.append(full_url)

# Remove duplicates
links = list(set(links))

print("\nTotal links:", len(links))

with open("data/raw/urls.txt", "w", encoding="utf-8") as f:

    for link in links:
        f.write(link + "\n")

print("URLs saved successfully!")