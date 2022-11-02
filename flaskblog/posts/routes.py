from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog import db  # imports from __init__.py since setup as a package in folder called 'flaskblog'
from flaskblog.posts.forms import PostForm # import from forms.py inside flaskblog package folder to be routed to templates for form inputs
from flaskblog.models import Post  # route db to templates e.g. User to register.html and login.html 
from flask_login import current_user, login_required  # import objects from flask_login to manage user authentication/sessions in templates 


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():  # Will send a POST request to this route 
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")  # Set route based on a variable. In this case post_id var set to be an int
def post(post_id):  # Receives post_id from the variable received in the route above 
    post = Post.query.get_or_404(post_id)  # Get post with post_id otherwise return 404 
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])  # Update post 
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # Get the post related to post_id  
    if post.author != current_user:  # Check the logged in user owns the post 
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data  # Update and save updated blog 
        post.content = form.content.data
        db.session.commit()  # Don't need to add to db with db.session.add since it already exists, just updating it         
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title  # pre-fill the create_post template with existing post data for update_post route here 
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')  # Same template new_post route but use legend as dynamic title 


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
    
