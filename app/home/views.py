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
    
    return render_template('home/contact.html', title="Contact Us", form=form)
    
@home.route('/dashboard-admin')
@login_required
def dashboard_admin():
    return render_template('home/dashboard-admin.html', title="Admin Dashboard")
    
@home.route('/dashboard-student')
@login_required
def dashboard_student():
    return render_template('home/dashboard-student.html', title="Student Dashboard")
    