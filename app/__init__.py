from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dupa123'

bs = Bootstrap(app)

from app import home
from .auth import auth
from app.exam.exam import examBp
from app.submission.submission import submissionBp

app.register_blueprint(auth.authBp)
app.register_blueprint(examBp)
app.register_blueprint(submissionBp)
