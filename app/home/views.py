from flask import flash, redirect, render_template, url_for, abort
from flask_login import login_required, current_user, login_user, logout_user


from . import home
from forms import ContactForm, LoginForm
from .. import db
from ..models import User, Checksheet, Contact, Announcement, ImportantDate
from app.decorators import check_confirmed
from app.email import send_email

@home.route('/', methods=['GET', 'POST'])
def homepage():
    
    dates = ImportantDate.query.all()
            
    return render_template('home/index.html', title="Home",dates=dates)
    
#route to contact page with contact form
@home.route('/contact', methods=['GET', 'POST'])
def contact():
    
    form = ContactForm()
    if form.validate_on_submit():
        #add send email to admin functionality
        contact = Contact(
            name = form.name.data,
            email = form.email.data,
            phone = form.phone.data,
            message = form.message.data,
        )
        db.session.add(contact)
        db.session.commit()
        
        html = render_template('home/confirm_contact.html', name=contact.name, email=contact.email, phone=contact.phone, message=contact.message)
        subject = "UMW Honors - Thank you for contacting us!"
        send_email(contact.email, subject, html)
        
        #change to redirect to success page
        flash('Contact form successfully submitted!', 'success')
        return redirect(url_for('home.contact'))
    
    return render_template('home/contact.html', title="Contact Us", form=form)
    
#route to user's dashboard
@home.route('/mypage')
@login_required
@check_confirmed
def mypage():
    
    announcements = Announcement.query.all()
    dates = ImportantDate.query.all()
    
    return render_template('home/mypage.html', title="My Page", announcements=announcements, dates=dates)


#route to user's checksheet
@home.route('/checksheet')
@login_required
@check_confirmed
def checksheet():
    user_honors_id = current_user.honors_id
    user_checksheet = Checksheet.query.filter_by(honors_id=user_honors_id).first()
    dates = ImportantDate.query.all()
   
    return render_template('home/view-checksheet.html', title="My Checksheet", checksheet=user_checksheet, dates=dates)


@home.route('/admin/dashboard')
@login_required
@check_confirmed
def admin_dashboard():

    if not current_user.is_admin:
        abort(403)
        
    announcements = Announcement.query.all()
    dates = ImportantDate.query.all()
    
    return render_template('home/admin_dashboard.html', title="Dashboard", announcements=announcements, dates=dates)
    