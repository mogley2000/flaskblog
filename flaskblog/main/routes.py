from flask import render_template, request, Blueprint
from flaskblog.models import Post  # route db to templates e.g. User to register.html and login.html 
from flask_login import login_user, current_user, login_required

main = Blueprint('main', __name__)


# App logic. @app decorators 
@main.route("/")
@main.route("/home")
@login_required  # protects the home page from being accessed without logging in. Redirects to user.login page as per __init__.py setup under .login_view = 'users.login' 
def home():
    # if current_user.is_authenticated:  # current_user function from flask_login package which gets the current_uesr logged in which relies on @login_manager in models.py
    #     return redirect(url_for('main.home'))  # If user already logged in, clicking login route redirects you to home instead of login since don't need to login again 
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()  # Check if email entered matches email stored in database. User.query is a method that links to the site.db file and checks all indexes             
    #     if user and bcrypt.check_password_hash(user.password, form.password.data):  #If user exists and password matches password in db
    #         login_user(user, remember=form.remember.data)  # Login user extension, Remember details true or false 
    #         next_page = request.args.get('next')  # if 'next' exists in url then next_page will be '/account' e.g. 'http://localhost:5000/login?next=%2Faccount'. 'next' shows up in url if you are blocked from accessing due to @login_required 
    #         return redirect(next_page) if next_page else redirect(url_for('main.home'))  # if next_page is not None, redirect to next_page i.e. the page you were trying to access but blocked by not login. otherwise after login, go to 'home'
    #         # Above is a ternary conditional 
    #     else:
    #         flash('Login Unsuccessful. Please check email and password', 'danger')
    # return render_template('login.html', title='Login', form=form)

    
    page = request.args.get('page', 1, type=int)  # variable for the page selected for posts var below, picked up as a request.args. type=int will throw value error if page is anything but an int. Default = 1. 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  # Instead of showing all posts i.e. Post.query.all() now query and return using paginate method to limit e.g. 5 posts per page. first arg selects page number e.g page 1 
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html')






