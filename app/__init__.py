from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dupa123'

bs = Bootstrap(app)

from app import home
from .auth import auth


app.register_blueprint(auth.authBp)