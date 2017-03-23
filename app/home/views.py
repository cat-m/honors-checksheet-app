from flask import flash, redirect, render_template, url_for, abort
from flask_login import login_required, current_user, login_user, logout_user, current_user


from . import home
from forms import ContactForm, LoginForm
from .. import db
from ..models import User

@home.route('/', methods=['GET', 'POST'])
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
    
#route to user's dashboard
@home.route('/mypage')
@login_required
def mypage():
    return render_template('home/mypage.html', title="My Page")

#route to user's checksheet
@home.route('/checksheet')
#@login_required
def checksheet():
    return render_template('home/view-checksheet.html', title="My Checksheet")



@home.route('/admin/dashboard')
@login_required
def admin_dashboard():

    if not current_user.is_admin:
        #throw a 403 error. we could do a custom error page later.
        abort(403)
    
    return render_template('home/admin_dashboard.html', title="Dashboard")
    