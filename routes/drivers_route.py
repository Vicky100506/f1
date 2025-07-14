from flask import Blueprint, jsonify, request
from models.drivers import db, Driver
from models.scrape_drivers import fetch_current_f1_drivers

drivers_bp = Blueprint("drivers", __name__, url_prefix="/drivers")


@drivers_bp.route("/", methods=["GET"])
def get_all_drivers():
    drivers = Driver.query.all()
    return jsonify([d.to_dict() for d in drivers]), 200


@drivers_bp.route("/<int:driver_id>", methods=["GET"])
def get_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    return jsonify(driver.to_dict()), 200


@drivers_bp.route("/", methods=["POST"])
def add_driver():
    data = request.get_json()
    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "name and age required"}), 400

    driver = Driver(
        name=data["name"],
        age=data["age"],
        profile_picture=data.get("profile_picture"),
        races_won=data.get("races_won", 0),
        podiums=data.get("podiums", 0),
        championships=data.get("championships", 0)
    )
    db.session.add(driver)
    db.session.commit()
    return jsonify(driver.to_dict()), 201


@drivers_bp.route("/<int:driver_id>", methods=["PUT"])
def update_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    data = request.get_json()

    driver.name = data.get("name", driver.name)
    driver.age = data.get("age", driver.age)
    driver.profile_picture = data.get("profile_picture", driver.profile_picture)
    driver.races_won = data.get("races_won", driver.races_won)
    driver.podiums = data.get("podiums", driver.podiums)
    driver.championships = data.get("championships", driver.championships)

    db.session.commit()
    return jsonify(driver.to_dict()), 200


@drivers_bp.route("/<int:driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return jsonify({"message": f"Driver {driver_id} deleted"}), 200


@drivers_bp.route("/scrape", methods=["POST"])
def scrape_drivers():
    """
    Trigger the scraping of drivers from formula1.com and save to DB
    """
    fetch_current_f1_drivers()
    return jsonify({"message": "Scraping complete and data saved"}), 200
