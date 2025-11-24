from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length


class ExamSearchForm(FlaskForm):
    examID = StringField(validators=[InputRequired(), Length(min=16, max=16)], render_kw={"placeholder": "Enter Exam ID"})

    submit = SubmitField('Search')

class ExamInitializationForm(FlaskForm):
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Enter Exam Password"})

    submit = SubmitField('Accept')