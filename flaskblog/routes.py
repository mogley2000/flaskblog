from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt  # imports from __init__.py since setup as a package in folder called 'flaskblog'
from flaskblog.forms import RegistrationForm, LoginForm  # import from forms.py inside flaskblog package folder 
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required  


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
    if form.validate_on_submit():  # If form is submitted correctly
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Setup hashed_password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # Setup new user using SQLAlchemy model imported frmo flaskblog.models. Call variables from form instance. 
        db.session.add(user)  # User staged for adding 
        db.session.commit()  # User committed to db 
        flash(f'Your account has been created for {form.username.data}!', 'success')  # flash is a flask method
        return redirect(url_for('login'))  # Return user back to 'login' route
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # If user already logged in, clicking login route redirects you to home instead of login since don't need to login again 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Check if email entered matches email stored in database            
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


@app.route("/account")
@login_required  # Extension requires us to login to access route. Define the login route in __init__.py 
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # image_file refers to default profile pic in models.py 
    return render_template('account.html', title='Account')
