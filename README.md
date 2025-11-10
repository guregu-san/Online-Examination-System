# Online-Examination-System


# how to use virtual environment
Packages:

Mac Command - pip3 install flask flask_sqlalchemy flask_login flask_bcrypt flask_wtf wtforms email_validator Flask-Bootstrap

Windows Command - pip install flask flask_sqlalchemy flask_login flask_bcrypt flask_wtf wtforms email_validator Flask-Bootstrap

env for python:

# 1) create venv (use .venv or venv as you prefer)
python3 -m venv .venv

# 2) activate venv
source .venv/bin/activate

# 3) upgrade pip, setuptools, wheel
python -m pip install --upgrade pip setuptools wheel

# 4) install the packages
pip install ...

# 5) quick verification
pip list
python -c "import flask, flask_sqlalchemy, flask_login; print('flask', flask.__version__)"
