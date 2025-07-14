from flask import Blueprint, request, jsonify
from models.User import db, User

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("/", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@user_bp.route("/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data or "age" not in data or "password" not in data:
        return jsonify({"error": "name, email, age, and password required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        age=data["age"],
        password=data["password"],
        profile_image=data.get("profile_image")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@user_bp.route("/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.age = data.get("age", user.age)
    user.profile_image = data.get("profile_image", user.profile_image)

    if "password" in data:
        user.password_hash = User.bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    db.session.commit()
    return jsonify(user.to_dict()), 200


@user_bp.route("/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} deleted"}), 200
