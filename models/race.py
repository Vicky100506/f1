# race.py

import requests
from bs4 import BeautifulSoup

def fetch_f1_race_circuits():
    url = 'https://www.formula1.com/en/racing/2025.html'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    race_data = []

    races = soup.find_all('a', class_='event-item-link')

    for race in races:
        try:
            title = race.find('div', class_='event-item__name').text.strip()
            location = race.find('div', class_='event-item__location').text.strip()
            image_tag = race.find('img')
            image_url = image_tag.get('data-src') or image_tag.get('src')

            race_data.append({
                'title': title,
                'location': location,
                'image_url': image_url
            })
        except Exception as e:
            continue

    return race_data
