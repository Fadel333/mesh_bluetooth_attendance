from flask import Flask, request, jsonify, render_template
from models import db, Student, Session, Attendance

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proximesh.db'
app.config['SECRET_KEY'] = 'secret'

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/api/checkin", methods=["POST"])
def checkin():

    data = request.json

    student_id = data["student_id"]
    group = data["group"]
    peers = data["peers_detected"]

    total = len(peers)

    matches = sum(1 for p in peers if p["group"] == group)

    match_rate = matches / total if total > 0 else 0

    verified = match_rate >= 0.6

    session = Session.query.filter_by(active=True).first()

    if verified and session:

        attendance = Attendance(
            student_id=student_id,
            session_id=session.id,
            match_rate=match_rate
        )

        db.session.add(attendance)
        db.session.commit()

    return jsonify({
        "verified": verified,
        "match_rate": match_rate,
        "matches": matches,
        "total": total
    })