from app import Courses, Students, Users, Admins, Instructors
import requests

def checkLogIn(user,password):
    print(user,password)
    document = Users.find_one({'user':user})
    if document:
        if document['password'] == password:
            return document['userID']
    return False

def getCourseDetails(CourseNumber):
    details = Courses.find_one({'Course Number': int(CourseNumber)})
    if not details:
        print(CourseNumber, type(CourseNumber))

    course = {
        'Name' : ''
    }
    course['Name'] = details['Title']
    course['Description'] = details['Description']
    course['Days'] = ''
    for day in details['Meeting']['Days']:
        course['Days'] += day + ', '

    course['StartTime'] = details['Meeting']['StartTime']
    course['EndTime'] = details['Meeting']['EndTime']
    course['icon'] = details['Icon']

    return course

def getStudentDetails(id):
    document = Students.find_one({'StudentID':id})
    #print('\n\n', id, '\n', document, '\n\n\n')
    name = document['Name']
    dob = document['DOB']
    address = document['Contact']['Address']
    phone = document['Contact']['PhoneNumber']
    email = document['Contact']['email']
    courseList = document['CourseList']
    courses = []
    for item in courseList:
        #print(item['CourseNumber'])
        courses.append(getCourseDetails(item['CourseNumber'])) 
        
    
    return name, dob, address, phone, email, courses

def getAllCourses():
    documents = Courses.find()
    courses = []
    
    for item in documents:
        course = {}
        course['subject'] = item['Subject']['Code']
        course['courseNumber'] = item['Course Number']
        course['name'] = item['Title']
        course['capacity'] = item['Status']['Capacity']
        course['enrolled'] = item['Status']['Enrolled']
        course['instructor'] = 'TBD'
        course['meeting'] = ''
        for day in item['Meeting']['Days']:
            course['meeting'] += day + ', '

        course['meeting'] += item['Meeting']['StartTime'] + '-' + item['Meeting']['EndTime']

        course['credits'] = item['Hours']

        courses.append(course.copy())
    
    return courses

def addCourse(id, CourseNumber):
    student = Students.find_one({'StudentID':id})
    student['CourseList'].append({
        'CourseNumber' : CourseNumber,
        'Subject' : 'CS',
        'Status' : 'Ongoing'
    })
    Students.update_one({'StudentID':id},{'$set':{'CourseList':student['CourseList']}})

    course = Courses.find_one({'Course Number':int(CourseNumber)})
    course['Status']['Enrolled'] += 1
    result = Courses.update_one({'Course Number':int(CourseNumber)},{'$set':{'Status':course['Status']}})

def dropCourse(id, CourseNumber):
    student = Students.find_one({'StudentID':id})
    courses = []
    for item in student['CourseList']:
        if int(item['CourseNumber']) == int(CourseNumber):
            removal = item
            continue

        courses.append(item)

    #student['CourseList'].remove(removal)
    Students.update_one({'StudentID':id},{'$set':{'CourseList':courses}})

    course = Courses.find_one({'Course Number':int(CourseNumber)})
    if course['Status']['Enrolled'] >0:
        course['Status']['Enrolled'] -= 1
        Courses.update_one({'Course Number':int(CourseNumber)},{'$set':{'Status':course['Status']}})

def checkDropCourse(id,CourseNumber):
    student = Students.find_one({'StudentID':id})
    for item in student['CourseList']:
        if int(item['CourseNumber']) == int(CourseNumber):
            return True
    
    return False

def checkAddCourses(id,CourseNumber):
    student = Students.find_one({'StudentID':id})
    course = Courses.find_one({'Course Number':int(CourseNumber)})

    for item in student['CourseList']:
        if int(item['CourseNumber']) == int(CourseNumber):
            return False
        
        doc = Courses.find_one({'Course Number':int(CourseNumber)})

        for day in course['Meeting']['Days']:
            if day in doc['Meeting']['Days']:
                if checkClass(course['Meeting']['StartTime'],course['Meeting']['EndTime'],doc['Meeting']['StartTime'],doc['Meeting']['EndTime']):
                    return False
                
    return True

# def checkClass(st1,et1,st2,et2):
#     if (st2 > st1 and st2 < et1) or (st1 > st2 and st1 < et2) :
#         return True
#     else:
#         return False
    
def checkClass(st1,et1,st2,et2):
    params = {
        'st1': st1,
        'et1': et1,
        'st2': st2,
        'et2': et2
    }
    response = requests.post("https://us-central1-unimanagementsystem-385301.cloudfunctions.net/check_class", json=params)
    if 'true' in response.text:
        return True
    else:
        return False

def getCredits(id):
    student = Students.find_one({'StudentID':id})
    return len(student['CourseList'])*3

def computeTuition(credits):
    return round(float(1000*credits),3)

def computeTotalFees(credits):
    return round(float(1260 + computeTuition(credits)),3)
