from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog import db, bcrypt # imports from __init__.py since setup as a package in folder called 'flaskblog'
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm  # import from forms.py inside flaskblog package folder to be routed to templates for form inputs
from flaskblog.models import User, Post  # route db to templates e.g. User to register.html and login.html 
from flask_login import login_user, current_user, logout_user, login_required  # import objects from flask_login to manage user authentication/sessions in templates 
from flaskblog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)  # similar to users = Flask(__name__). Pass in name of blueprint 'users'. Create 
                                      # a Blueprint object called users 


@users.route("/register", methods=['GET', 'POST'])  # Route needs to be able to POST to register 
def register():
    if current_user.is_authenticated: # If user already logged in, clicking register route redirects you to home instead of login since don't need to login again 
        return redirect(url_for('main.home'))
    form = RegistrationForm()  # Instantiate class imported from form.py 
    if form.validate_on_submit():  # If form is submitted correctly, add the new user to db. 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Setup hashed_password from pw input via form 
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # Setup new user using SQLAlchemy model imported frmo flaskblog.models. Call variables from form instance. 
        db.session.add(user)  # User staged for adding 
        db.session.commit()  # User committed to db 
        flash(f'Your account has been created for {form.username.data}!', 'success')  # flash is a flask method
        return redirect(url_for('users.login'))  # Return user back to 'login' route
    
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])  # when '/login' route is called, will step through the below. e.g. check current_user, try login user
def login():
    if current_user.is_authenticated:  # current_user function from flask_login package which gets the current_uesr logged in which relies on @login_manager in models.py
        return redirect(url_for('main.home'))  # If user already logged in, clicking login route redirects you to home instead of login since don't need to login again 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Check if email entered matches email stored in database. User.query is a method that links to the site.db file and checks all indexes             
        if user and bcrypt.check_password_hash(user.password, form.password.data):  #If user exists and password matches password in db
            login_user(user, remember=form.remember.data)  # Login user extension, Remember details true or false 
            next_page = request.args.get('next')  # if 'next' exists in url then next_page will be '/account' e.g. 'http://localhost:5000/login?next=%2Faccount'. 'next' shows up in url if you are blocked from accessing due to @login_required 
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  # if next_page is not None, redirect to next_page i.e. the page you were trying to access but blocked by not login. otherwise after login, go to 'home'
            # Above is a ternary conditional 
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])  # methods allows you to POST back to the route and recieve data from forms
@login_required  # Extension requires us to login to access route. 
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
        return redirect(url_for('users.account'))  # redirect before getting to render_template prevents re-POST on reload. Instead passes a GET request 
    
    elif request.method == 'GET':  # will populate form with existing current_user data when /account route is called as a 'GET' i.e. link to 'GET' the page, not 'POST' on submit 
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # current_user.image_file refers to default profile pic in models.py. current_user is flask_login package  
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")  # show posts for only specific username
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # variable for the page selected for posts var below, picked up as a request.args. type=int will throw value error if page is anything but an int. Default = 1. 
    user = User.query.filter_by(username=username).first_or_404() # get first user with this username or 404. username from the route variable 
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)  
    return render_template('user_posts.html', posts=posts, user=user)
    

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:  # current_user function from flask_login package which gets the current_uesr logged in which relies on @login_manager in models.py
        return redirect(url_for('main.home'))  # If user already logged in, clicking login route redirects you to home instead of login since don't need to login again 
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:  # current_user function from flask_login package which gets the current_uesr logged in which relies on @login_manager in models.py
        return redirect(url_for('main.home'))  # If user already logged in, clicking login route redirects you to home instead of login since don't need to login again 
    user = User.verify_reset_token(token) # call the method under the User model verify_reset_token 
    if user is None: #verify_reset_token should return user_id. If not, flash warning
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():  # If form is submitted correctly, add the new user to db. 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Setup hashed_password from pw input via form 
        user.password = hashed_password
        db.session.commit()  # user.password update committed to db 
        flash(f'Your password has been updated', 'success')  # flash is a flask method
        return redirect(url_for('users.login'))  # Return user back to 'login' route
   
    return render_template('reset_token.html', title='Reset Password', form=form)
