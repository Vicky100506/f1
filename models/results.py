import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL
base_url = "https://www.formula1.com"
results_url = f"{base_url}/en/results.html/2024/races.html"

# Fetch the races list page
r = requests.get(results_url)
soup = BeautifulSoup(r.text, "html.parser")

# Get all race links
race_links = soup.select("a.resultsarchive-filter-item-link")
races = []

for link in race_links:
    race_name = link.get_text(strip=True)
    race_href = link.get("href")
    full_url = base_url + race_href

    # Fetch individual race result page
    r2 = requests.get(full_url)
    soup2 = BeautifulSoup(r2.text, "html.parser")

    # Grab the results table
    table = soup2.find("table", class_="resultsarchive-table")
    if table:
        rows = table.find_all("tr")[1:]  # skip header

        winner_row = rows[0]  # 1st place
        cols = winner_row.find_all("td")

        position = cols[1].get_text(strip=True)
        driver = cols[2].get_text(strip=True)
        car = cols[3].get_text(strip=True)
        laps = cols[4].get_text(strip=True)
        time = cols[5].get_text(strip=True)

        races.append({
            "Race": race_name,
            "Position": position,
            "Driver": driver,
            "Team": car,
            "Laps": laps,
            "Time/Gap": time
        })
    else:
        print(f"⚠️ No results table found for {race_name} — likely not run yet.")

# Save to DataFrame
df = pd.DataFrame(races)

print("\n🏁 F1 2024 Race Winners:")
print(df)

# Save to CSV
df.to_csv("f1_2024_race_results.csv", index=False)
print("\n✅ Results saved to f1_2024_race_results.csv")
