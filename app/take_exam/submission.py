'''IGNORE THIS FOR NOW BECAUSE IT MIGHT NOT BE NEEDED'''
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey

db = SQLAlchemy()

class Submission(db.Model):
    __tablename__ = "submissions"

    submission_id = db.Column(db.Integer, primary_key=True)

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("exams.exam_id"),
        nullable=False
    )

    roll_number = db.Column(
        db.String,
        db.ForeignKey("students.roll_number"),
        nullable=False
    )

    started_at = db.Column(db.DateTime, default=None)
    submitted_at = db.Column(db.DateTime, default=None)
    updated_at = db.Column(db.DateTime, default=None)

    feedback = db.Column(db.Text)
    answers = db.Column(db.Text)

    status = db.Column(
        db.String,
        CheckConstraint(
            "status IN ('IN_PROGRESS', 'SUBMITTED', 'IN_REVIEW', 'GRADED')"
        ),
        default="IN_PROGRESS"
    )

    total_score = db.Column(db.Integer)

    # Optional: SQLAlchemy relationship helpers
    exam = db.relationship("Exam", backref="submissions")
    student = db.relationship("Student", backref="submissions")

    def __repr__(self):
        return f"<Submission {self.submission_id} | exam={self.exam_id} | student={self.roll_number}>"
