from flask_restful import Resource
from flask import request
from models import db, Question, Answer, Exam

# U3-F3: Add Question (with validation)
class AddQuestion(Resource):
    def post(self):
        data = request.get_json()
        exam_id = data.get("exam_id")
        question_text = data.get("question_text")
        question_type = data.get("question_type")
        answers = data.get("answers", [])

        exam = Exam.query.get(exam_id)
        if not exam:
            return {"error": "Exam not found"}, 404

        # Determine next order index
        max_index = db.session.query(db.func.max(Question.order_index)).filter_by(exam_id=exam_id).scalar()
        next_index = (max_index or 0) + 1

        question = Question(
            exam_id=exam_id,
            question_text=question_text,
            question_type=question_type,
            order_index=next_index
        )
        db.session.add(question)
        db.session.flush()

        if question_type in ["MCQ_SINGLE", "MCQ_MULTIPLE", "TRUE_FALSE"]:
            for ans in answers:
                new_answer = Answer(
                    question_id=question.question_id,
                    answer_text=ans["answer_text"],
                    is_correct=ans.get("is_correct", False)
                )
                db.session.add(new_answer)

        db.session.commit()
        return {"message": "Question added successfully", "question_id": question.question_id}


# U3-F4: Edit Question
class EditQuestion(Resource):
    def put(self, question_id):
        data = request.get_json()
        question = Question.query.get(question_id)
        if not question:
            return {"error": "Question not found"}, 404

        new_text = data.get("question_text", question.question_text)
        new_type = data.get("question_type", question.question_type)
        new_answers = data.get("answers", [])

        question.question_text = new_text
        question.question_type = new_type

        # Remove old answers
        Answer.query.filter_by(question_id=question_id).delete()

        if new_type in ["MCQ_SINGLE", "MCQ_MULTIPLE", "TRUE_FALSE"]:
            for ans in new_answers:
                new_answer = Answer(
                    question_id=question_id,
                    answer_text=ans["answer_text"],
                    is_correct=ans.get("is_correct", False)
                )
                db.session.add(new_answer)

        db.session.commit()
        return {"message": "Question updated successfully"}


# U3-F5: Delete Question
class DeleteQuestion(Resource):
    def delete(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            return {"error": "Question not found"}, 404

        # Delete all related answers
        Answer.query.filter_by(question_id=question_id).delete()
        db.session.delete(question)
        db.session.commit()

        return {"message": "Question deleted successfully"}
