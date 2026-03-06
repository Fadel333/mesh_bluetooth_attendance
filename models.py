from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))  # student / lecturer
    student_id = db.Column(db.String(20))
    device_id = db.Column(db.String(120))


class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(120))
    group_id = db.Column(db.Integer)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    leader_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"))
    status = db.Column(db.String(20))  # verified / pending / flagged
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)