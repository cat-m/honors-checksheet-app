from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from . import home
from forms import ContactForm


@home.route('/')
def homepage():
    return render_template('home/index.html', title="Home")
    
@home.route('/contact', methods=['GET', 'POST'])
def contact():
    
    form = ContactForm()
    if form.validate_on_submit():
        #add send email to admin functionality
        #change to redirect to success page
        return redirect(url_for('home.contact'))
    
    return render_template('home/contact.html', form=form)
    
@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title="Admin Dashboard")
    