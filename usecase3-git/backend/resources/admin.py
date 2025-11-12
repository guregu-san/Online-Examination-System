from flask_restful import Resource
from models import db, Exam, Question, Answer

# U3-F10: IT Support Functions

# 🧩 Verify Exam Integrity
class AdminVerifyExam(Resource):
    def get(self, exam_id):
        exam = Exam.query.get(exam_id)
        if not exam:
            return {"error": "Exam not found"}, 404

        issues = []
        for q in exam.questions:
            # Check question type validity
            if q.question_type not in ["MCQ_SINGLE", "MCQ_MULTIPLE", "TRUE_FALSE", "SHORT_ANSWER", "NUMERICAL", "ESSAY"]:
                issues.append(f"Question {q.question_id} has invalid type: {q.question_type}")

            # Check answers exist if needed
            if q.question_type in ["MCQ_SINGLE", "MCQ_MULTIPLE", "TRUE_FALSE"] and len(q.answers) == 0:
                issues.append(f"Question {q.question_id} has no answers for type {q.question_type}")

        if not issues:
            return {"message": "Exam integrity verified. No issues found."}
        else:
            return {"message": "Integrity check completed.", "issues": issues}


# 🧩 Restore Deleted Exam (simplified version)
class AdminRestoreExam(Resource):
    def post(self):
        # Simulated restore logic (you can expand this later)
        data = {"status": "restored", "message": "Deleted exam restored from backup (simulation)."}
        return data, 200
