import sqlite3
import json
from flask import Blueprint, request, jsonify, render_template
from app import app



# DB connection
def get_db():
    conn = sqlite3.connect("oesDB.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Blueprint setup
exam_viewBp = Blueprint('exam_view', __name__, template_folder='templates')
@app.route('/exams', methods=['GET'])
def view_exams():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()
    conn.close()
    return render_template('view_exams.html', exams=exams)

# API endpoint to get exams in JSON format
@exam_viewBp.route('/api/exams', methods=['GET'])
def api_get_exams():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()
    exams_list = [dict(exam) for exam in exams]
    conn.close()
    return jsonify(exams_list)

app.register_blueprint(exam_viewBp)
