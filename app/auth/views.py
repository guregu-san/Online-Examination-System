from flask import flash


@auth.route('/')
def home():
    return "Welcome to the Home Page!"