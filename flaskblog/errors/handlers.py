from django.shortcuts import render
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)  #Different decorator to deal with error handling vs route 
def error_404(error):
    return render_template('errors/404.html'), 404  # returns second vaue which is 404 status code. Default is 200. 


@errors.app_errorhandler(403)  
def error_403(error):
    return render_template('errors/403.html'), 403   


@errors.app_errorhandler(500)  
def error_500(error):
    return render_template('errors/500.html'), 500  