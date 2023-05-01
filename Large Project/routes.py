from app import app, db
from flask import render_template, url_for, flash, get_flashed_messages, redirect, request
from datetime import datetime
from flask import Blueprint
from forms import ManagegeCourseForm, LogInForm
import forms,utils

main = Blueprint('main', __name__)

#import models
#import forms

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    print('In Login')
    form = LogInForm()
    message = ''
    if form.is_submitted():
        print('validated')
        user = form.user.data
        password = form.password.data
        id = utils.checkLogIn(user,password)

        if id:
            return redirect(location='/home/'+id)
        else:
            message = 'Incorrect Username or Password'
            return render_template('login.html',form=form, message=message)
    
    print('Not validated')
        
    return render_template('login.html', form=form, message=message)

@app.route('/home/<id>')
def home(id):
    name, dob, address, phone, email, courses = utils.getStudentDetails(id)
    print(courses)
    return render_template('home.html', id = id, name=name, dob=dob, address=address, phone=phone, email=email, courses=courses)

@app.route('/courses/<id>', methods=['GET', 'POST'])
def courses(id):
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
                return redirect('/home/'+id)
            else:
                message = 'Cannot add course. Clashing times or course already added'
                return render_template('manageCourse.html', form=form, courses = courses, message= message, id = id)
            
        if form.drop.data:
            if utils.checkDropCourse(id,course):
                utils.dropCourse(id, course)
                #redirect(url_for('home', id = id))
                return redirect('/home/'+id)
            else:
                message = 'Cannot drop a course that has not been taken'
                return render_template('manageCourse.html', form=form, courses = courses, message = message, id = id)

    return render_template('manageCourse.html', form=form, courses = courses, message = message, id = id)

@app.route('/payments/<id>')
def payments(id):
    credits = utils.getCredits(id)
    tuition = utils.computeTuition(credits)
    total = utils.computeTotalFees(credits)
    return render_template('payments.html', id = id, credits = credits, tuition = tuition, total = total)
