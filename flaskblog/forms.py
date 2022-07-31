from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):  #FlaskForm as an argument to inherit from FlaskForm 
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Catch non-unique username at the form stage. Method will run when instance is created. }
    def validate_username(self, username):  # Function inside a class is a method 
        """ Check username isn't already in User db """
        user = User.query.filter_by(username=username.data).first()  # Check username.data from form is already in User db
        if user:  # If user is anything other than None
            raise ValidationError('That username is already taken. Please choose another username')

    def validate_email(self, email):
        """ Check email isn't already in User db """
        user = User.query.filter_by(email=email.data).first()  # Check username.data from form is already in User db
        if user:  # If user is anything other than None
            raise ValidationError('That email is already taken. Please choose another email')


class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

