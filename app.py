from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Import models and scraping functions
from models.drivers import Driver, db as driver_db
from models.team import Team, db as team_db
from models.User import User, db as user_db, bcrypt
from models.race import fetch_f1_race_circuits
from models.results import df as race_results
from models.shedule import df as race_schedule
from models.predictions import predicted_podium

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///f1_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
driver_db.init_app(app)
team_db.init_app(app)
user_db.init_app(app)
bcrypt.init_app(app)

# Create DB tables
with app.app_context():
    driver_db.create_all()
    team_db.create_all()
    user_db.create_all()

# Routes

@app.route('/')
def home():
    return jsonify({"message": "🏁 Welcome to F1 API"})

@app.route('/drivers')
def get_drivers():
    drivers = Driver.query.all()
    return jsonify([d.to_dict() for d in drivers])

@app.route('/teams')
def get_teams():
    teams = Team.query.all()
    return jsonify([t.to_dict() for t in teams])

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route('/circuits')
def get_circuits():
    data = fetch_f1_race_circuits()
    return jsonify(data)

@app.route('/results')
def get_results():
    return race_results.to_json(orient="records")

@app.route('/schedule')
def get_schedule():
    return race_schedule.to_json(orient="records")

@app.route('/predicted_podium')
def get_podium():
    return jsonify({"predicted_podium": predicted_podium})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
