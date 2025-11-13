from flask import Flask, render_template
from app import app

@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')