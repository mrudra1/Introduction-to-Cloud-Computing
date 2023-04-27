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
Workers = db['Workers']

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)