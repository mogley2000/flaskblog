from flask import render_template, request, Blueprint
from flaskblog.models import Post  # route db to templates e.g. User to register.html and login.html 

main = Blueprint('main', __name__)


# App logic. @app decorators 
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)  # variable for the page selected for posts var below, picked up as a request.args. type=int will throw value error if page is anything but an int. Default = 1. 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  # Instead of showing all posts i.e. Post.query.all() now query and return using paginate method to limit e.g. 5 posts per page. first arg selects page number e.g page 1 
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html')






