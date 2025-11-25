from app import app
from flask import Blueprint, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from app.auth.form import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../oesDB.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
authBp = Blueprint("authBp", __name__, template_folder="templates")

db =  SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Students(db.Model):
    roll_number = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    contact_number = db.Column(db.Integer, nullable=True)

class Instructors(db.Model):
    instructor_id = db.Column(db.Integer, primary_key=True, nullable=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)


@authBp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
        
    return render_template('login.html', form=form)


@authBp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        role = form.role.data or 'student'
        if role == 'student':
            if not form.roll_number.data or not form.contact_number.data:
                return render_template('register.html', form=form)
            
        if role == 'student':
            student = Students(
                roll_number = form.roll_number.data,
                name = form.name.data,
                email = form.email.data,
                password_hash = bcrypt.generate_password_hash(form.password.data),
                contact_number = form.contact_number.data,
            )
            db.session.add(student)
        else:
            instructor = Instructors(
                name = form.name.data,
                email = form.email.data,
                password_hash = bcrypt.generate_password_hash(form.password.data),


            )
            db.session.add(instructor)

        db.session.commit()
        return redirect(url_for('authBp.login'))

    return render_template('register.html', form=form)