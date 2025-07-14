import requests
from bs4 import BeautifulSoup

url = "https://www.formula1.com/en/results.html/2024/drivers.html"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

with open("page.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("✅ Saved page.html — open it and check if the table is there.")
