from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, ValidationError, Optional, Email
from app.auth.models import Students, Instructors



class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    role = RadioField('Role', choices=[('Student'), ('Instructor')], default='Student')
    roll_number = StringField(validators=[Optional()], render_kw={"placeholder": "Roll Number"})
    name = StringField(validators=[Optional(), Length(min=2, max=50)], render_kw={"placeholder": "Name"})
    contact_number = StringField(validators=[Optional(), Length(min=10, max=15)], render_kw={"placeholder": "Contact Number"})
    
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        role = self.role.data or 'student'
        if role == 'student':
            existing_user_email = Students.query.filter_by(email=email.data).first()
        else:
            existing_user_email = Instructors.query.filter_by(email=email.data).first()
        
        if existing_user_email:
            raise ValidationError("That email address is already in use. Please choose a different one.")