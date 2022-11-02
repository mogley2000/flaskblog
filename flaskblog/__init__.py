# __init__.py is loaded automatically and referred to as 'from flaskblog import create_app' e.g. refer to run.py 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager  # provides user session mgmt for Flask. Handles logging in, log out, remember users 
from flask_mail import Mail 
from flaskblog.config import Config  # app configs stored in the Config class in config.py 


# Extensions - need to stay outside the create_app func below due to Flask requirements to initialise separately 
db = SQLAlchemy()  # Instance of SQLAlchemy db - you need to create an instance in Flask every time 
bcrypt = Bcrypt() # password hashing 
login_manager = LoginManager() # instantiate instance of LoginManager object and link it to flask app
login_manager.login_view = 'users.login'  # pass in function name of route for login. Required for login_required decorator in routes.py e.g. same as url_for. 
                                    #  Need this to stop /account from loading if not logged in per routes.py and instead redirects to 'login' to ask you to login
login_manager.login_message_category = 'info'  # SEt Bootstrap category for the default 'Please login to access this page' flash message shown by this extenbsion, 

# Setup lost password package flask_mail - CURRENTLY DOES NOT WORK AS GMAIL NO LONGER ACCEPTS 3RD PARTY ACCESS [June2022]
mail = Mail()






# Create function to load different configuration objects for the application
def create_app(config_class=Config):  #imported from config.py class. default = Config 
    app = Flask(__name__)  # Instantiate an instance of Flask which is part of the Class 
    app.config.from_object(Config) #import configs from Class 
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from flaskblog.users.routes import users  
    from flaskblog.posts.routes import posts  
    from flaskblog.main.routes import main  
    from flaskblog.errors.handlers import errors # import instance of the errors Blueprint 
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app