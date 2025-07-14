import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the F1 2024 schedule page
url = "https://www.formula1.com/en/racing/2024.html"

# Get the page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all race cards
race_cards = soup.find_all('a', class_='event-item-wrapper')

schedule = []

for race in race_cards:
    race_name = race.find('span', class_='event-title').get_text(strip=True)
    race_date = race.find('span', class_='date').get_text(strip=True)
    race_location = race.find('span', class_='event-location').get_text(strip=True)

    schedule.append({
        'Race': race_name,
        'Date': race_date,
        'Location': race_location
    })

# Create DataFrame
df = pd.DataFrame(schedule)

print("🏎️ F1 2024 Schedule:")
print(df)

# Optional: Save to CSV
df.to_csv('f1_2024_schedule.csv', index=False)
print("\n✅ Schedule saved to f1_2024_schedule.csv")
