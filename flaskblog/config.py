import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  #secret key using 'import secrets' to encrypt cookies and save send them to browser for unique sessions 
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')   # Will create a site.db in root directory 
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # Username and pw for forgotpwserver@gmail.com saved locally in PATH
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
