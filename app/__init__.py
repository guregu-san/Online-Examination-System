'''Third-party packages'''
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dupa123'

bs = Bootstrap(app)

'''Local packages'''
from app import home
from .auth import auth
from app.exam.exam import examBp
from .take_exam import take_exam
from .view_exams import exam_viewBp

app.register_blueprint(auth.authBp)
app.register_blueprint(examBp)
app.register_blueprint(take_exam.takeExamBp)
app.register_blueprint(exam_viewBp)