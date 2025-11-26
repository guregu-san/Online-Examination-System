from flask import Flask, render_template
from app import app
from flask_login import login_required, current_user

@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

'''
@app.route('/take_exam', methods=['GET', 'POST'])
def takeExam():
    return render_template('submission.html')
'''