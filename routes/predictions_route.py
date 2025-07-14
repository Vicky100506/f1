import requests
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sqlite3
import datetime
import sys

# ============================
# STEP 1: Scrape data
# ============================

def fetch_f1_standings():
    """
    Scrape current F1 standings from official F1 website.
    """
    url = "https://www.formula1.com/en/results.html/2024/drivers.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find("table", class_="resultsarchive-table")
    if table is None:
        print("❌ Could not find standings table. Check the page structure.")
        sys.exit(1)

    rows = table.find_all("tr")[1:]  # skip header

    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue
        position = int(cols[1].text.strip())
        driver = cols[2].text.strip()
        nationality = cols[3].text.strip()
        team = cols[4].text.strip()
        points = float(cols[5].text.strip())

        data.append([position, driver, nationality, team, points])

    df = pd.DataFrame(data, columns=['Position', 'Driver', 'Nationality', 'Team', 'Points'])
    return df


df = fetch_f1_standings()

print("📋 Data Sample:")
print(df.head())

# ============================
# STEP 2: Prepare data
# ============================

df['DriverID'] = LabelEncoder().fit_transform(df['Driver'])
df['TeamID'] = LabelEncoder().fit_transform(df['Team'])

# Feature: Points + Team
X = df[['Points', 'TeamID']]
y = df['DriverID']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ============================
# STEP 3: Train model
# ============================

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\n✅ Model accuracy (on current standings): {acc:.2f}")

# ============================
# STEP 4: Predict podium
# ============================

# Assume next race will have similar conditions
next_race_features = X.sort_values(by='Points', ascending=False).iloc[:3]

podium_preds = clf.predict(next_race_features)

inverse_driver = dict(zip(df['DriverID'], df['Driver']))

print("\n🔮 Predicted Podium for Next Race:")
predicted_podium = []
for idx, pred in enumerate(podium_preds, 1):
    driver_name = inverse_driver[pred]
    predicted_podium.append(driver_name)
    print(f"{idx}. {driver_name}")

# ============================
# STEP 5: Save to SQLite
# ============================

conn = sqlite3.connect("f1_predictions.db")
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    driver TEXT,
    position INTEGER,
    points REAL,
    team TEXT,
    predicted_podium TEXT
)
''')

# Insert current standings
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for _, row in df.iterrows():
    c.execute('''
    INSERT INTO predictions (timestamp, driver, position, points, team, predicted_podium)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        timestamp,
        row['Driver'],
        row['Position'],
        row['Points'],
        row['Team'],
        ", ".join(predicted_podium)  # same podium saved for each row
    ))

conn.commit()
conn.close()

print("\n📁 Standings & predictions saved to `f1_predictions.db` ✅")
