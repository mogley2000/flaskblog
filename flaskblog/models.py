from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin 

@login_manager.user_loader  # Per docs to setup login manager 
def load_user(user_id):
    return User.query.get(int(user_id))



# Create db models that reflect structure of db 
class User(db.Model, UserMixin):  # Inherit from db.Model. UserMixin is required. 
    id = db.Column(db.Integer, primary_key=True) # User id 
    username = db.Column(db.String(20), unique=True, nullable=False) # Username, 20 char length max, must be unique, must have at least a username
    email = db.Column(db.String(120), unique=True, nullable=False) # Email
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # Profile pic
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) # backref allows Post to get the user that created the post. Every post must have a User. But a User can have many Posts. 

    def __repr__(self):
        """ How messages are printed """
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

# Variables required for templates 
