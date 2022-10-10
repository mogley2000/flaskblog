import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager  # provides user session mgmt for Flask. Handles logging in, log out, remember users 
from flask_mail import Mail 

app = Flask(__name__)  # Instantiate an instance of Flask which is part of the Class 
# Flask configs
app.config['SECRET_KEY'] = '37c12260a96d750bcf641726e24a219d'  #secret key using 'import secrets' to encrypt cookies and save send them to browser for unique sessions 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'   # Relative location. Will create a site.db in root directory 


db = SQLAlchemy(app)  # Instance of SQLAlchemy db - you need to create an instance in Flask every time 
bcrypt = Bcrypt(app) # password hashing 
login_manager = LoginManager(app) # instantiate instance of LoginManager object and link it to flask app
login_manager.login_view = 'users.login'  # pass in function name of route for login. Required for login_required decorator in routes.py e.g. same as url_for. 
                                    #  Need this to stop /account from loading if not logged in per routes.py and instead redirects to 'login' to ask you to login
login_manager.login_message_category = 'info'  # SEt Bootstrap category for the default 'Please login to access this page' flash message shown by this extenbsion, 

# Setup lost password package flask_mail - CURRENTLY DOES NOT WORK AS GMAIL NO LONGER ACCEPTS 3RD PARTY ACCESS [June2022]
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # Username and pw for forgotpwserver@gmail.com saved locally in PATH
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)



from flaskblog.users.routes import users  
from flaskblog.posts.routes import posts  
from flaskblog.main.routes import main  

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
