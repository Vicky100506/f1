from flask import Blueprint, jsonify, request
from models.team import db, Team, fetch_current_f1_teams

team_bp = Blueprint("teams", __name__, url_prefix="/teams")


@team_bp.route("/", methods=["GET"])
def get_all_teams():
    teams = Team.query.all()
    return jsonify([t.to_dict() for t in teams]), 200


@team_bp.route("/<int:team_id>", methods=["GET"])
def get_team(team_id):
    team = Team.query.get_or_404(team_id)
    return jsonify(team.to_dict()), 200


@team_bp.route("/", methods=["POST"])
def add_team():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400

    if Team.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Team already exists"}), 400

    team = Team(
        name=data["name"],
        picture=data.get("picture"),
        championships=data.get("championships", 0),
        years_active=data.get("years_active", 0),
        races_won=data.get("races_won", 0)
    )
    db.session.add(team)
    db.session.commit()
    return jsonify(team.to_dict()), 201


@team_bp.route("/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    team = Team.query.get_or_404(team_id)
    data = request.get_json()

    team.name = data.get("name", team.name)
    team.picture = data.get("picture", team.picture)
    team.championships = data.get("championships", team.championships)
    team.years_active = data.get("years_active", team.years_active)
    team.races_won = data.get("races_won", team.races_won)

    db.session.commit()
    return jsonify(team.to_dict()), 200


@team_bp.route("/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({"message": f"Team {team_id} deleted"}), 200


@team_bp.route("/scrape", methods=["POST"])
def scrape_teams():
    """
    Trigger scraping of current F1 teams from formula1.com and save to DB
    """
    fetch_current_f1_teams()
    return jsonify({"message": "Scraping complete and teams saved"}), 200
