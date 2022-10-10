from datetime import datetime
from xml.dom import NoModificationAllowedErr
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from flaskblog import db, login_manager  # Setup as instantiated objects in __init__.py. App allows secret key to be imported for use in reset token 
from flask_login import UserMixin 
from flask import current_app

@login_manager.user_loader  # Per docs to setup login manager using a decorator on top of the load_user func 
def load_user(user_id):
    return User.query.get(int(user_id))


# Create db models that reflect structure of db 
class User(db.Model, UserMixin):  # Inherit from db.Model. UserMixin is required. 
    id = db.Column(db.Integer, primary_key=True) # User id 
    username = db.Column(db.String(20), unique=True, nullable=False) # Username, 20 char length max, must be unique, must have at least a username
    email = db.Column(db.String(120), unique=True, nullable=False) # Email
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')  # Profile pic
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) # backref allows Post to get the user that created the post. Every post must have a User. But a User can have many Posts. 

    def get_reset_token(self, expires_sec=1800):  # Method to get reset email token
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')  # payload is current user_id as dict
    
    @staticmethod  # Decorator because self is not used as a argument 
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """ How messages are printed to be machine-readable when __repr__ is called on an instance of a Class
         e.g. print(repr(user)). https://www.pythontutorial.net/python-oop/python-__repr__/ """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):  # Inherit from db.Model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# to create db: 
# enter REPL 
# from flaskblog import db
# db.create_all() -> create site.db
# from flaskblog import User, Post
# user_1 = User(username='Leo', email='leo@gmail.com', password='password')
# db.session.add(user_1)
# user_2 = User(username='Spam', email='spam@gmail.com', password='password')
# db.session.add(user_2)
# db.session.commit()

# Need to include this code into routes.py and templates to allow manipulation from flaskblog 
