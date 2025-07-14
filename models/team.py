import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    picture = db.Column(db.String(200), nullable=True)
    championships = db.Column(db.Integer, default=0)
    years_active = db.Column(db.Integer, default=0)
    races_won = db.Column(db.Integer, default=0)

    def __init__(self, name, picture=None, championships=0, years_active=0, races_won=0):
        self.name = name
        self.picture = picture
        self.championships = championships
        self.years_active = years_active
        self.races_won = races_won

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "championships": self.championships,
            "years_active": self.years_active,
            "races_won": self.races_won
        }

# 🔍 Scrape only current teams from F1.com

def fetch_current_f1_teams():
    url = "https://www.formula1.com/en/teams.html"
    headers = {"User-Agent": "Mozilla/5.0"}  # Some websites block requests without user-agent
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")
    team_blocks = soup.select(".f1-logo-listing--link")

    if not team_blocks:
        print("No current F1 teams found.")
        return

    for block in team_blocks:
        name = block.select_one(".f1-logo-listing--name")
        image = block.select_one("img")

        if name and image:
            team_name = name.text.strip()
            logo_url = image['data-src'] if 'data-src' in image.attrs else image['src']

            # Add to DB only if not already present
            if not Team.query.filter_by(name=team_name).first():
                team = Team(name=team_name, picture=logo_url)
                db.session.add(team)

    db.session.commit()
    print("Current F1 teams scraped and added.")
