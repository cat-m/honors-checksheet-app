from flask import render_template
from flask_login import login_required

from . import home

@home.route('/')
def homepage():
    return render_template('home/index.html', title="Home")
    
@home.route('/contact')
def contact():
    return render_template('home/contact.html')
    
@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title="Admin Dashboard")
    
