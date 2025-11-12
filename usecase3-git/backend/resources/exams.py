from flask_restful import Resource
from flask import request
from models import db, Exam, Instructor, Course, Question, Answer
from datetime import datetime

# U3-F2: Create New Exam
class CreateExam(Resource):
    def post(self):
        data = request.get_json()
        instructor_email = data.get("instructor_email")
        course_code = data.get("course_code")
        title = data.get("title", "Untitled Exam")

        instructor = Instructor.query.filter_by(email=instructor_email).first()
        course = Course.query.filter_by(course_code=course_code).first()

        if not instructor or not course:
            return {"error": "Invalid instructor or course"}, 400

        exam = Exam(
            course_id=course.course_id,
            instructor_id=instructor.instructor_id,
            title=title,
            created_at=datetime.utcnow(),
        )
        db.session.add(exam)
        db.session.commit()

        return {"message": "Exam created successfully", "exam_id": exam.exam_id}, 201


# U3-F7: Set Exam Options
class SetExamOptions(Resource):
    def put(self, exam_id):
        data = request.get_json()
        time_limit = data.get("time_limit")
        security_settings = data.get("security_settings")

        exam = Exam.query.get(exam_id)
        if not exam:
            return {"error": "Exam not found"}, 404

        exam.time_limit = time_limit
        exam.security_settings = security_settings
        exam.updated_at = datetime.utcnow()
        db.session.commit()

        return {"message": "Exam settings updated"}


# U3-F8: Save Exam (update existing questions/answers)
class SaveExam(Resource):
    def put(self, exam_id):
        data = request.get_json()
        title = data.get("title", None)
        time_limit = data.get("time_limit", None)
        security_settings = data.get("security_settings", None)
        questions = data.get("questions", [])

        exam = Exam.query.get(exam_id)
        if not exam:
            return {"error": "Exam not found"}, 404

        if title:
            exam.title = title
        if time_limit:
            exam.time_limit = time_limit
        if security_settings:
            exam.security_settings = security_settings
        exam.updated_at = datetime.utcnow()

        # Replace all questions for simplicity
        Question.query.filter_by(exam_id=exam_id).delete()
        db.session.commit()

        for q in questions:
            new_q = Question(
                exam_id=exam_id,
                question_text=q["question_text"],
                question_type=q["question_type"],
                order_index=q.get("order_index", 0),
            )
            db.session.add(new_q)
            db.session.flush()
            for a in q.get("answers", []):
                ans = Answer(
                    question_id=new_q.question_id,
                    answer_text=a["answer_text"],
                    is_correct=a.get("is_correct", False),
                )
                db.session.add(ans)

        db.session.commit()
        return {"message": "Exam saved successfully"}


# U3-F9: Retrieve Instructor Exams
class GetInstructorExams(Resource):
    def get(self, instructor_id):
        exams = Exam.query.filter_by(instructor_id=instructor_id).all()
        data = [
            {
                "exam_id": e.exam_id,
                "title": e.title,
                "course": e.course.course_name,
                "created_at": e.created_at,
            }
            for e in exams
        ]
        return {"exams": data}


# Retrieve full exam (for editor)
class GetExam(Resource):
    def get(self, exam_id):
        exam = Exam.query.get(exam_id)
        if not exam:
            return {"error": "Exam not found"}, 404

        exam_data = {
            "exam_id": exam.exam_id,
            "title": exam.title,
            "time_limit": exam.time_limit,
            "security_settings": exam.security_settings,
            "questions": [],
        }

        for q in exam.questions:
            q_data = {
                "question_id": q.question_id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "order_index": q.order_index,
                "answers": [],
            }
            for a in q.answers:
                q_data["answers"].append(
                    {"answer_id": a.answer_id, "answer_text": a.answer_text, "is_correct": a.is_correct}
                )
            exam_data["questions"].append(q_data)

        return exam_data


# U3-F6: Reorder Questions
class ReorderQuestions(Resource):
    def put(self, exam_id):
        data = request.get_json()
        order = data.get("order", [])

        for item in order:
            q = Question.query.get(item["question_id"])
            if q:
                q.order_index = item["order_index"]
        db.session.commit()

        return {"message": "Question order updated"}
