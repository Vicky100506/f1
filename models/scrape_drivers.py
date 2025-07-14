import requests
from bs4 import BeautifulSoup


def fetch_current_f1_drivers():
    from drivers import Driver, db
    url = 'https://www.formula1.com/en/drivers.html'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    drivers_section = soup.select('a.f1-driver')

    for driver_tag in drivers_section:
        name_tag = driver_tag.select_one('.f1-driver__name')
        if name_tag:
            full_name = name_tag.text.strip()

            image_tag = driver_tag.select_one('img.f1-driver__photo')
            profile_picture = image_tag['data-src'] if image_tag and image_tag.has_attr('data-src') else None

            existing = Driver.query.filter_by(name=full_name).first()
            if not existing:
                new_driver = Driver(
                    name=full_name,
                    age=0,  # unknown
                    profile_picture=profile_picture,
                    races_won=0,
                    podiums=0,
                    championships=0
                )
                db.session.add(new_driver)

    db.session.commit()
    print("Driver data imported.")


if __name__ == "__main__":
    fetch_current_f1_drivers() 