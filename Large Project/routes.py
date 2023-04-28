from app import app, db
from flask import render_template, url_for, flash, get_flashed_messages, redirect, request
from datetime import datetime
from flask import Blueprint
from forms import ManagegeCourseForm, LogInForm
import forms,utils

main = Blueprint('main', __name__)

#import models
#import forms

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    message = ''
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        id = utils.checkLogIn(user,password)

        if id:
            return redirect(location='/home/'+id)
        else:
            message = 'Incorrect Username or Password'
            return render_template('login.html',form=form, message=message)
        
    return render_template('login.html', form=form, message=message)

@app.route('/home/<id>')
def home(id):
    name, dob, address, phone, email, courses = utils.getStudentDetails(id)
    return render_template('home.html', name, dob, address, phone, email, courses)

@app.route('/courses/<id>', methods=['GET', 'POST'])
def add(id):
    form = ManagegeCourseForm()
    courses = utils.getAllCourses()
    message = ''
    #print('\n\n\n',form.title.__call__(),'Hello')
    if form.validate_on_submit():
        subject = form.subject.data
        course = form.courseNumber.data

        if form.add.data:
            if utils.checkAddCourses(id,course):
                utils.addCourse(id,course)
                redirect(url_for('home',id = id))
            else:
                message = 'Cannot add course. Clashing times'
                return render_template('add.html', form=form, courses = courses, message= message)
            
        if form.drop.data:
            if utils.checkDropCourse(id,course):
                utils.dropCourse(id, course)
                redirect(url_for('home', id = id))
            else:
                message = 'Cannot drop a course that has not been taken'
                return render_template('add.html', form=form, courses = courses, message = message)

    return render_template('manageCourse.html', form=form, courses = courses, message = message)

@main.route('/payments')
def payments():
    return render_template('payments.html')
