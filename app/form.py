from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, ValidationError, Optional, Email
from app import views


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    role = RadioField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher')], default='student')
    roll_number = StringField(validators=[Optional()], render_kw={"placeholder": "Roll Number"})
    name = StringField(validators=[Optional(), Length(min=2, max=50)], render_kw={"placeholder": "Name"})
    contact_number = StringField(validators=[Optional(), Length(min=10, max=15)], render_kw={"placeholder": "Contact Number"})
    
    submit = SubmitField('Register')