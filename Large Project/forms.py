from datetime import datetime
from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, HiddenField, StringField, widgets, SelectField, PasswordField
from wtforms.validators import DataRequired
import uuid

class ManagegeCourseForm(FlaskForm):
    subject = SelectField('Subject',choices=[('CS','Computer Science')])
    courseNumber = SelectField('CourseNumber', choices=[('520','520'),('526','526'),('532','532'),('535','535'),('536','536'),('550','550'),('565','565'),('571','571'),('572','572'),('575','575')],validators=[DataRequired()])
    add = SubmitField('Add')
    drop = SubmitField('Drop')

class LogInForm(FlaskForm):
    user = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('Submit', id = 'submit')