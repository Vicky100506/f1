from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    profile_picture = db.Column(db.String(200), nullable=True)
    races_won = db.Column(db.Integer, default=0)
    podiums = db.Column(db.Integer, default=0)
    championships = db.Column(db.Integer, default=0)

    def __init__(self, name, age, profile_picture=None, races_won=0, podiums=0, championships=0):
        self.name = name
        self.age = age
        self.profile_picture = profile_picture
        self.races_won = races_won
        self.podiums = podiums
        self.championships = championships

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "profile_picture": self.profile_picture,
            "races_won": self.races_won,
            "podiums": self.podiums,
            "championships": self.championships
        }
