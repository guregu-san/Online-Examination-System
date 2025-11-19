import sqlite3
import json
from flask import Blueprint, request, jsonify

submissionBp = Blueprint("submissionBp", __name__, url_prefix="/submission")

def get_db():
    conn = sqlite3.connect("oesDB.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def row_to_dict(row):
    return {k: row[k] for k in row.keys()}

def calculate_score(exam_id, answers_dict):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT question_id, points FROM questions WHERE exam_id=?", (exam_id,))
    questions = cur.fetchall()

    total_score = 0

    for q in questions:
        qid = q["question_id"]
        key = str(qid)

        selected = answers_dict.get(key, [])
        if isinstance(selected, int):
            selected = [selected]
        selected = set(map(int, selected)) if selected else set()

        cur.execute("SELECT option_id, is_correct FROM options WHERE question_id=?", (qid,))
        rows = cur.fetchall()
        correct = {r["option_id"] for r in rows if r["is_correct"] == 1}

        if selected == correct and len(correct) > 0:
            total_score += q["points"]

    conn.close()
    return total_score

# Start Exam
@submissionBp.route("/<int:exam_id>/start", methods=["POST"])
def start_exam(exam_id):
    data = request.get_json(silent=True) or {}
    roll_number = data.get("roll_number")

    if not roll_number:
        return jsonify(error="roll_number required"), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT exam_id FROM exams WHERE exam_id=?", (exam_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify(error="Exam not found"), 404

    cur.execute("SELECT roll_number FROM students WHERE roll_number=?", (roll_number,))
    if not cur.fetchone():
        conn.close()
        return jsonify(error="Student not found"), 404

    # Check if submission exists already
    cur.execute("""
        SELECT submission_id, status
        FROM submissions
        WHERE exam_id=? AND roll_number=?
        ORDER BY started_at DESC
    """, (exam_id, roll_number))
    row = cur.fetchone()

    if row and row["status"] in ("IN_PROGRESS", "SUBMITTED", "GRADED"):
        conn.close()
        return jsonify(
            error="Submission already exists",
            submission_id=row["submission_id"],
            status=row["status"]
        ), 400

    # Create new submission
    cur.execute("""
        INSERT INTO submissions (exam_id, roll_number, started_at, status, answers, total_score)
        VALUES (?, ?, CURRENT_TIMESTAMP, 'IN_PROGRESS', ?, 0)
    """, (exam_id, roll_number, json.dumps({})))

    sid = cur.lastrowid
    conn.commit()
    conn.close()

    return jsonify(message="Exam started", submission_id=sid), 201

# Save Progress
@submissionBp.route("/<int:exam_id>/save", methods=["PATCH"])
def save_progress(exam_id):
    data = request.get_json(silent=True) or {}
    roll_number = data.get("roll_number")
    answers = data.get("answers")

    if not roll_number:
        return jsonify(error="roll_number required"), 400
    if answers is None:
        return jsonify(error="answers required"), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT submission_id FROM submissions
        WHERE exam_id=? AND roll_number=? AND status='IN_PROGRESS'
    """, (exam_id, roll_number))

    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify(error="Active submission not found"), 404

    cur.execute("""
        UPDATE submissions
        SET answers=?, updated_at=CURRENT_TIMESTAMP
        WHERE submission_id=?
    """, (json.dumps(answers), row["submission_id"]))

    conn.commit()
    conn.close()

    return jsonify(message="Progress saved"), 200

# Submit Exam
@submissionBp.route("/<int:exam_id>/submit", methods=["POST"])
def submit_exam(exam_id):
    data = request.get_json(silent=True) or {}
    roll_number = data.get("roll_number")
    final_answers = data.get("answers")

    if not roll_number:
        return jsonify(error="roll_number required"), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT submission_id, answers, status
        FROM submissions
        WHERE exam_id=? AND roll_number=?
        ORDER BY started_at DESC
    """, (exam_id, roll_number))

    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify(error="Submission not found"), 404

    if row["status"] in ("SUBMITTED", "GRADED"):
        conn.close()
        return jsonify(error="Exam already submitted"), 400

    current_answers = json.loads(row["answers"]) if row["answers"] else {}
    merged_answers = final_answers if final_answers else current_answers

    total = calculate_score(exam_id, merged_answers)

    cur.execute("""
        UPDATE submissions
        SET answers=?, submitted_at=CURRENT_TIMESTAMP,
            status='GRADED', total_score=?, updated_at=CURRENT_TIMESTAMP
        WHERE submission_id=?
    """, (json.dumps(merged_answers), total, row["submission_id"]))

    conn.commit()
    conn.close()

    return jsonify(message="Submitted and graded", total_score=total), 200

# Check Status
@submissionBp.route("/<int:exam_id>/status", methods=["GET"])
def submission_status(exam_id):
    roll_number = request.args.get("roll_number")

    if not roll_number:
        return jsonify(error="roll_number required"), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT submission_id, status, started_at,
               submitted_at, total_score
        FROM submissions
        WHERE exam_id=? AND roll_number=?
    """, (exam_id, roll_number))

    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify(error="Submission not found"), 404

    return jsonify(row_to_dict(row)), 200
