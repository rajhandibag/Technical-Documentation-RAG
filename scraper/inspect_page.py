import requests
from bs4 import BeautifulSoup

url = "https://docs.python.org/3/library/"

response = requests.get(url)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

document = soup.find("div", class_="document")

documentwrapper = document.find(
    "div",
    class_="documentwrapper"
)

bodywrapper = documentwrapper.find(
    "div",
    class_="bodywrapper"
)

print("\nBODYWRAPPER CHILDREN:\n")

for child in bodywrapper.find_all(recursive=False):
    print(
        child.name,
        "class =", child.get("class"),
        "id =", child.get("id")
    )