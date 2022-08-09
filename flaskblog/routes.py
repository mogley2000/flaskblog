""" routes.py routes app code to html templates and ability to pass outputs of code and vars into templates. 
e.g. Also executes addition of new users to db in registration route after receiving form inputs via
registration.html which validates using forms created in forms.py """

import secrets, os 
from PIL import Image  # Pillow app to resize profile pics 
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt  # imports from __init__.py since setup as a package in folder called 'flaskblog'
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm  # import from forms.py inside flaskblog package folder to be routed to templates for form inputs
from flaskblog.models import User, Post  # route db to templates e.g. User to register.html and login.html 
from flask_login import login_user, current_user, logout_user, login_required  # import objects from flask_login to manage user authentication/sessions in templates 


posts = [
    {
        'author': 'Monkey',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Rabbit',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

# App logic. @app decorators 
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])  # Route needs to be able to POST to register 
def register():
    if current_user.is_authenticated: # If user already logged in, clicking register route redirects you to home instead of login since don't need to login again 
        return redirect(url_for('home'))
    form = RegistrationForm()  # Instantiate class imported from form.py 
    if form.validate_on_submit():  # If form is submitted correctly, add the new user to db. 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Setup hashed_password from pw input via form 
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # Setup new user using SQLAlchemy model imported frmo flaskblog.models. Call variables from form instance. 
        db.session.add(user)  # User staged for adding 
        db.session.commit()  # User committed to db 
        flash(f'Your account has been created for {form.username.data}!', 'success')  # flash is a flask method
        return redirect(url_for('login'))  # Return user back to 'login' route
    
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])  # when '/login' route is called, will step through the below. e.g. check current_user, try login user
def login():
    if current_user.is_authenticated:  # current_user function from flask_login package which gets the current_uesr logged in which relies on @login_manager in models.py
        return redirect(url_for('home'))  # If user already logged in, clicking login route redirects you to home instead of login since don't need to login again 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Check if email entered matches email stored in database. User.query is a method that links to the site.db file and checks all indexes             
        if user and bcrypt.check_password_hash(user.password, form.password.data):  #If user exists and password matches password in db
            login_user(user, remember=form.remember.data)  # Login user extension, Remember details true or false 
            next_page = request.args.get('next')  # if 'next' exists in url then next_page will be '/account' e.g. 'http://localhost:5000/login?next=%2Faccount'. 'next' shows up in url if you are blocked from accessing due to @login_required 
            return redirect(next_page) if next_page else redirect(url_for('home'))  # if next_page is not None, redirect to next_page i.e. the page you were trying to access but blocked by not login. otherwise after login, go to 'home'
            # Above is a ternary conditional 
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):  # Data from uploaded pic has a .filename attribute 
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # Concetenate the file name extension. 
    picture_fn = random_hex + f_ext  # picture filenamne
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)  # Where to save profile pics 

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn 

@app.route("/account", methods=['GET', 'POST'])  # methods allows you to POST back to the route and recieve data from forms
@login_required  # Extension requires us to login to access route. Define the login route in __init__.py 
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():  # Will send a POST request to this route 
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data  #  Enables form input to update current_user db .username and .email and then commit to db 
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')  # 'success' is bootstrap class 
        return redirect(url_for('account'))  # redirect before getting to render_template prevents re-POST on reload. Instead passes a GET request 
    
    elif request.method == 'GET':  # will populate form with existing current_user data when /account route is called as a 'GET' i.e. link to 'GET' the page, not 'POST' on submit 
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # current_user.image_file refers to default profile pic in models.py. current_user is flask_login package  
    return render_template('account.html', title='Account', image_file=image_file, form=form)
