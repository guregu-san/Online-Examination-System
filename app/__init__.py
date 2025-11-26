'''Third-party packages'''
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dupa123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../oesDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bs = Bootstrap(app)
db.init_app(app)
bcrypt.init_app(app)

'''Local packages'''
from app import home
from app.auth.auth import authBp
from app.exam.exam import examBp
from .take_exam import take_exam
from .view_exams import exam_viewBp

app.register_blueprint(authBp)
app.register_blueprint(examBp)
app.register_blueprint(take_exam.takeExamBp)
app.register_blueprint(exam_viewBp)