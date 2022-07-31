from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager  # provides user session mgmt for Flask. Handles logging in, log out, remember users 


app = Flask(__name__)  # Instantiate an instance of Flask which is part of the Class 
# Flask configs
app.config['SECRET_KEY'] = '37c12260a96d750bcf641726e24a219d'  #secret key using 'import secrets' to encrypt cookies and save send them to browser for unique sessions 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'   # Relative location 
db = SQLAlchemy(app)  # Instance of SQLAlchemy db 
bcrypt = Bcrypt(app) # password hashing 
login_manager = LoginManager(app)  
login_manager.login_view = 'login'  # pass in function name of route for login. Required for login_required decorator in routes.py e.g. same as url_for. Need this to stop /account from loading if not logged in per routes.py
login_manager.login_message_category = 'info'  # SEt Bootstrap category for the default 'Please login to access this page' flash message shown by this extenbsion, 


from flaskblog import routes  # avoid circular imports so have below 