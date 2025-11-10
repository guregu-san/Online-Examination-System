from app import app
from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap

from app.form import LoginForm


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