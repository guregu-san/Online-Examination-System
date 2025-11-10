from app import app
from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap

from app.form import LoginForm, RegisterForm


@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
        
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        role = form.role.data or 'student'
        if role == 'student':
            if not form.name.data or not form.contact_number.data:
                return render_template('register.html', form=form)

        return redirect(url_for('login'))

    return render_template('register.html', form=form)