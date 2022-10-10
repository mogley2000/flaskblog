import secrets, os 
from PIL import Image  # Pillow app to resize profile pics 
from flask import url_for, current_app 
from flask_mail import Message
from flaskblog import mail  # imports from __init__.py since setup as a package in folder called 'flaskblog'


def save_picture(form_picture):  # Data from uploaded pic has a .filename attribute 
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # Concetenate the file name extension. 
    picture_fn = random_hex + f_ext  # picture filenamne
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # Where to save profile pics 

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn 

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your pw, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}'''

    mail.send(msg)


