from app import app
from flask import Blueprint, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from app.auth.form import LoginForm, RegisterForm

authBp = Blueprint("authBp", __name__, template_folder="templates")

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
            if not form.name.data or not form.contact_number.data:
                return render_template('register.html', form=form)

        return redirect(url_for('authBp.login'))

    return render_template('register.html', form=form)