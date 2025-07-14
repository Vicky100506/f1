from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup

schedule_bp = Blueprint("schedule", __name__)

@schedule_bp.route("/f1/schedule", methods=["GET"])
def get_f1_schedule():
    """
    Scrape the current F1 race schedule from the official site.
    """
    url = "https://www.formula1.com/en/racing/2024.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    schedule = []

    # Locate race list elements (adjust these selectors if site structure changes!)
    race_cards = soup.select(".race-card")  # Example class, adjust if needed.

    if not race_cards:
        return jsonify({"error": "Could not find race schedule on the page"}), 500

    for card in race_cards:
        race_name = card.select_one(".raceTitle")
        race_date = card.select_one(".date")
        race_location = card.select_one(".circuit-info")

        schedule.append({
            "Race": race_name.get_text(strip=True) if race_name else "N/A",
            "Date": race_date.get_text(strip=True) if race_date else "N/A",
            "Location": race_location.get_text(strip=True) if race_location else "N/A",
        })

    return jsonify({
        "message": "🏎️ F1 2024 Schedule",
        "schedule": schedule
    })
