from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    symptoms = db.relationship('Symptom', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom_list = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Symptom {self.symptom_list}>'
