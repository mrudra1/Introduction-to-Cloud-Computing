from flask import Flask
from flask_recaptcha import ReCaptcha
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

# app.config['RECAPTCHA_SITE_KEY'] = '6LcIEeIgAAAAAMjypLNll4TLQFyOscswLP1HME2p' 
# app.config['RECAPTCHA_SECRET_KEY'] = '6LcIEeIgAAAAAPdgrg_om-RqkOrpzqtgMCu2-9_R'
# recaptcha = ReCaptcha(app)

client = MongoClient("mongodb+srv://manjarirudra:BgxHnvE5REtpYngG@cluster0.4awsnp7.mongodb.net/?retryWrites=true&w=majority")
db = client['UMS']
Courses = db['Courses']
Students = db['Students']
Instructors = db['Instructors']
Admins = db['Admins']
Users = db['Users']

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)