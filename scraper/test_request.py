import requests
from bs4 import BeautifulSoup

url = "https://docs.python.org/3/"

response = requests.get(url)

if response.status_code != 200:
    print("Failed:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

content = soup.find("div", class_="document")

if content:
    text = content.get_text("\n", strip=True)

    with open("data/raw/python_docs.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("Data saved successfully")

else:
    print("Documentation content not found")