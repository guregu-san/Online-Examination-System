from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
from resources.exams import CreateExam, GetExam, SetExamOptions, SaveExam, ReorderQuestions, GetInstructorExams
from resources.questions import AddQuestion, EditQuestion, DeleteQuestion
from resources.instructors import LoadExamCreation
from resources.admin import AdminVerifyExam, AdminRestoreExam

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exam_app.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
db.init_app(app)
api = Api(app)

# Register endpoints
api.add_resource(LoadExamCreation,   "/api/instructor/<string:email>")
api.add_resource(CreateExam,         "/api/exams")
api.add_resource(AddQuestion,        "/api/questions")
api.add_resource(EditQuestion,       "/api/questions/<int:question_id>")
api.add_resource(DeleteQuestion,     "/api/questions/<int:question_id>")
api.add_resource(ReorderQuestions,   "/api/exams/<int:exam_id>/reorder")
api.add_resource(SetExamOptions,     "/api/exams/<int:exam_id>/options")
api.add_resource(SaveExam,           "/api/exams/<int:exam_id>")
api.add_resource(GetInstructorExams, "/api/instructors/<int:instructor_id>/exams")
api.add_resource(GetExam,            "/api/exams/<int:exam_id>/detail")
api.add_resource(AdminVerifyExam,    "/api/admin/verify/<int:exam_id>")
api.add_resource(AdminRestoreExam,   "/api/admin/restore")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)
