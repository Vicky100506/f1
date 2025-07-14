# user.py

import random
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def generate_hex_id():
    """Generate a unique 16-bit hex ID as a string."""
    while True:
        hex_id = format(random.randint(0, 0xFFFF), '04X')  # e.g., '1A3F'
        existing = User.query.get(hex_id)
        if not existing:
            return hex_id

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(4), primary_key=True)  # 16-bit HEX ID (max 4 characters)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(200), nullable=True)

    def __init__(self, name, email, age, password, profile_image=None):
        self.id = generate_hex_id()
        self.name = name
        self.email = email
        self.age = age
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profile_image = profile_image

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "profile_image": self.profile_image
        }
