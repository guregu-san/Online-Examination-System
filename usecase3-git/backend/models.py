from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Instructor(db.Model):
    __tablename__ = "instructors"
    instructor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    courses = db.relationship("Course", backref="instructor", lazy=True)
    exams = db.relationship("Exam", backref="instructor", lazy=True)


class Course(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey("instructors.instructor_id"), nullable=False)

    exams = db.relationship("Exam", backref="course", lazy=True)


class Exam(db.Model):
    __tablename__ = "exams"
    exam_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey("instructors.instructor_id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    time_limit = db.Column(db.Integer)
    security_settings = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    questions = db.relationship("Question", backref="exam", lazy=True, cascade="all, delete-orphan")


class Question(db.Model):
    __tablename__ = "questions"
    question_id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.exam_id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    order_index = db.Column(db.Integer, default=0)

    answers = db.relationship("Answer", backref="question", lazy=True, cascade="all, delete-orphan")


class Answer(db.Model):
    __tablename__ = "answers"
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
