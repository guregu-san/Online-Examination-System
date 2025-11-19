import sqlite3
import json
from flask import Blueprint, request, jsonify, render_template


# Blueprint
examBp = Blueprint("examBp", __name__, url_prefix="/exams", template_folder="../templates")


# DB helper
def get_db():
    conn = sqlite3.connect("oesDB.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def row_to_dict(row):
    return {k: row[k] for k in row.keys()}


# U3-F1: Create exam
@examBp.route("", methods=["POST"])
def create_exam():
    """
    Create a new exam for an existing course + instructor.
    Expects JSON:
    {
      "course_code": "CS101",
      "instructor_email": "teacher@uni.com",
      "title": "Midterm",
      "time_limit": 90,
      "security_settings": "shuffle=true"
    }
    """
    data = request.get_json(silent=True) or {}
    course_code = data.get("course_code")
    instructor_email = data.get("instructor_email")
    title = data.get("title", "Untitled Exam")
    time_limit = data.get("time_limit")
    security_settings = data.get("security_settings", "")

    if not course_code or not instructor_email:
        return jsonify(error="course_code and instructor_email are required"), 400

    conn = get_db()
    cur = conn.cursor()

    # validate instructor
    cur.execute("SELECT email FROM instructors WHERE email = ?", (instructor_email,))
    if not cur.fetchone():
        conn.close()
        return jsonify(error="Instructor does not exist"), 400

    # validate course
    cur.execute("SELECT course_code, instructor_email FROM courses WHERE course_code = ?", (course_code,))
    course = cur.fetchone()
    if not course:
        conn.close()
        return jsonify(error="Course does not exist"), 400

    # optionally, enforce that course belongs to instructor_email
    if course["instructor_email"] != instructor_email:
        conn.close()
        return jsonify(error="Instructor is not assigned to this course"), 400

    # create exam
    cur.execute(
        """
        INSERT INTO exams (course_code, instructor_email, title, time_limit, security_settings,
                           created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (course_code, instructor_email, title, time_limit, security_settings),
    )

    exam_id = cur.lastrowid
    conn.commit()
    conn.close()

    return jsonify(message="Exam created", exam_id=exam_id), 201


# U3-F2: Add question to exam
@examBp.route("/<int:exam_id>/questions", methods=["POST"])
def add_question(exam_id):
    """
    Adds a question and its options to an exam.
    JSON:
    {
      "question_text": "...",
      "is_multiple_correct": false,
      "points": 5,
      "options": [
        {"option_text": "A", "is_correct": false},
        {"option_text": "B", "is_correct": true}
      ]
    }
    """
    data = request.get_json(silent=True) or {}
    question_text = data.get("question_text")
    is_multiple_correct = data.get("is_multiple_correct", False)
    points = int(data.get("points", 1))
    options = data.get("options", [])

    if not question_text:
        return jsonify(error="question_text is required"), 400
    if not isinstance(options, list) or len(options) == 0:
        return jsonify(error="At least one option is required"), 400

    # normalize boolean
    if isinstance(is_multiple_correct, str):
        is_multiple_correct = is_multiple_correct.lower() in ("true", "1", "yes", "on")

    conn = get_db()
    cur = conn.cursor()

    # validate exam exists
    cur.execute("SELECT exam_id FROM exams WHERE exam_id = ?", (exam_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify(error="Exam not found"), 404

    # if single-correct, ensure exactly one correct option
    correct_count = sum(1 for opt in options if opt.get("is_correct"))
    if not is_multiple_correct and correct_count != 1:
        conn.close()
        return jsonify(error="Single-correct question must have exactly one correct option"), 400

    # determine order_index
    cur.execute("SELECT COALESCE(MAX(order_index), 0) FROM questions WHERE exam_id = ?", (exam_id,))
    current_max = cur.fetchone()[0]
    order_index = current_max + 1

    # insert question
    cur.execute(
        """
        INSERT INTO questions (exam_id, question_text, is_multiple_correct, points, order_index)
        VALUES (?, ?, ?, ?, ?)
        """,
        (exam_id, question_text, int(is_multiple_correct), points, order_index),
    )
    question_id = cur.lastrowid

    # insert options
    for opt in options:
        cur.execute(
            """
            INSERT INTO options (question_id, option_text, is_correct)
            VALUES (?, ?, ?)
            """,
            (
                question_id,
                opt.get("option_text", ""),
                1 if opt.get("is_correct") else 0,
            ),
        )

    # update exam updated_at
    cur.execute("UPDATE exams SET updated_at = CURRENT_TIMESTAMP WHERE exam_id = ?", (exam_id,))
    conn.commit()
    conn.close()

    return jsonify(message="Question added", question_id=question_id), 201


# U3-F3: Edit question
@examBp.route("/questions/<int:question_id>", methods=["PATCH"])
def edit_question(question_id):
    """
    Edit question text / points / is_multiple_correct and optionally
    replace all options.
    """
    data = request.get_json(silent=True) or {}

    conn = get_db()
    cur = conn.cursor()

    # find exam_id from question
    cur.execute("SELECT exam_id FROM questions WHERE question_id = ?", (question_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify(error="Question not found"), 404
    exam_id = row["exam_id"]

    fields = []
    values = []

    if "question_text" in data:
        fields.append("question_text = ?")
        values.append(data["question_text"])

    if "points" in data:
        fields.append("points = ?")
        values.append(int(data["points"]))

    if "is_multiple_correct" in data:
        val = data["is_multiple_correct"]
        if isinstance(val, str):
            val = val.lower() in ("true", "1", "yes", "on")
        fields.append("is_multiple_correct = ?")
        values.append(1 if val else 0)

    if fields:
        sql = f"UPDATE questions SET {', '.join(fields)} WHERE question_id = ?"
        values.append(question_id)
        cur.execute(sql, values)

    # Replace options if provided
    if "options" in data:
        options = data["options"]
        if not isinstance(options, list) or not options:
            conn.close()
            return jsonify(error="options must be a non-empty list"), 400

        # enforce single-correct logic based on current is_multiple_correct
        cur.execute("SELECT is_multiple_correct FROM questions WHERE question_id = ?", (question_id,))
        qrow = cur.fetchone()
        is_multiple_correct = bool(qrow["is_multiple_correct"])
        correct_count = sum(1 for o in options if o.get("is_correct"))
        if not is_multiple_correct and correct_count != 1:
            conn.close()
            return jsonify(error="Single-correct question must have exactly one correct option"), 400

        cur.execute("DELETE FROM options WHERE question_id = ?", (question_id,))
        for opt in options:
            cur.execute(
                """
                INSERT INTO options (question_id, option_text, is_correct)
                VALUES (?, ?, ?)
                """,
                (
                    question_id,
                    opt.get("option_text", ""),
                    1 if opt.get("is_correct") else 0,
                ),
            )

    # update exam updated_at
    cur.execute("UPDATE exams SET updated_at = CURRENT_TIMESTAMP WHERE exam_id = ?", (exam_id,))
    conn.commit()
    conn.close()

    return jsonify(message="Question updated"), 200


# U3-F4: Delete question
@examBp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT exam_id FROM questions WHERE question_id = ?", (question_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify(error="Question not found"), 404
    exam_id = row["exam_id"]

    cur.execute("DELETE FROM options WHERE question_id = ?", (question_id,))
    cur.execute("DELETE FROM questions WHERE question_id = ?", (question_id,))
    cur.execute("UPDATE exams SET updated_at = CURRENT_TIMESTAMP WHERE exam_id = ?", (exam_id,))

    conn.commit()
    conn.close()

    return jsonify(message="Question deleted"), 200


# U3-F5: Reorder questions
@examBp.route("/<int:exam_id>/reorder", methods=["POST"])
def reorder_questions(exam_id):
    data = request.get_json(silent=True) or {}
    order = data.get("order", [])

    if not isinstance(order, list):
        return jsonify(error="order must be a list"), 400

    conn = get_db()
    cur = conn.cursor()

    # ensure exam exists
    cur.execute("SELECT exam_id FROM exams WHERE exam_id = ?", (exam_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify(error="Exam not found"), 404

    for item in order:
        qid = item.get("question_id")
        idx = item.get("order_index")
        if qid is None or idx is None:
            continue
        cur.execute(
            "UPDATE questions SET order_index = ? WHERE question_id = ? AND exam_id = ?",
            (int(idx), int(qid), exam_id),
        )

    cur.execute("UPDATE exams SET updated_at = CURRENT_TIMESTAMP WHERE exam_id = ?", (exam_id,))
    conn.commit()
    conn.close()

    return jsonify(message="Order updated"), 200


# U3-F6: Update exam options
@examBp.route("/<int:exam_id>/options", methods=["PATCH"])
def update_exam_options(exam_id):
    data = request.get_json(silent=True) or {}
    fields = []
    values = []

    if "title" in data:
        fields.append("title = ?")
        values.append(data["title"])

    if "time_limit" in data:
        fields.append("time_limit = ?")
        values.append(int(data["time_limit"]))

    if "security_settings" in data:
        fields.append("security_settings = ?")
        values.append(data["security_settings"])

    if not fields:
        return jsonify(message="No changes"), 200

    sql = f"""
        UPDATE exams
        SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
        WHERE exam_id = ?
    """
    values.append(exam_id)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT exam_id FROM exams WHERE exam_id = ?", (exam_id,))
    if not cur.fetchone():
        conn.close()
        return jsonify(error="Exam not found"), 404

    cur.execute(sql, values)
    conn.commit()
    conn.close()

    return jsonify(message="Exam options updated"), 200


# U3-F7: List exams by instructor
@examBp.route("/instructor/<path:email>", methods=["GET"])
def list_exams_by_instructor(email):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT exam_id, title, course_code, time_limit, security_settings,
               created_at, updated_at
        FROM exams
        WHERE instructor_email = ?
        ORDER BY created_at DESC
        """,
        (email,),
    )
    rows = cur.fetchall()
    conn.close()

    return jsonify([row_to_dict(r) for r in rows]), 200
