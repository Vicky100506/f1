from flask import Blueprint, jsonify
from models.race import fetch_f1_race_circuits

race_bp = Blueprint("races", __name__, url_prefix="/races")


@race_bp.route("/scrape", methods=["GET"])
def scrape_races():
    """
    Scrape the current season's race circuits and return as JSON
    """
    races = fetch_f1_race_circuits()
    if not races:
        return jsonify({"error": "Failed to fetch race data"}), 500
    return jsonify({"races": races, "count": len(races)}), 200
