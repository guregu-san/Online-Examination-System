from flask_restful import Resource
from flask import request
from models import db, Instructor, Course

# U3-F1: Load Exam Creation Page
class LoadExamCreation(Resource):
    def get(self, email):
        instructor = Instructor.query.filter_by(email=email).first()
        if not instructor:
            return {"status": "denied", "reason": "Instructor not found"}, 403
        return {
            "status": "ok",
            "instructor_id": instructor.instructor_id,
            "email": instructor.email,
            "courses": [
                {"course_id": c.course_id, "course_code": c.course_code, "course_name": c.course_name}
                for c in instructor.courses
            ],
        }
