from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Students(db.Model):
    roll_number = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    contact_number = db.Column(db.Integer, nullable=True)

class Instructors(db.Model):
    instructor_id = db.Column(db.Integer, primary_key=True, nullable=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)