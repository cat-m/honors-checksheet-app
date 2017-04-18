from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user
import datetime
from . import auth
from forms import LoginForm, RegistrationForm, ResetPasswordForm, ChangePasswordForm, ResetPasswordEmailForm
from .. import db
from ..models import User, ImportantDate
from ..token import generate_confirmation_token, confirm_token
from app.email import send_email

#check that token created and email matches an email in the database
@auth.route('/confirm/<token>')
#@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except: 
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else: 
        user.is_confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thank You!', 'success')
        
    #return redirect(url_for('home.mypage'))
    return redirect(url_for('auth.login'))

#check that user token created and email matches email in database
@auth.route('/update-password/<token>', methods=['GET', 'POST'])
def update_password(token):
    try:
        email = confirm_token(token)
    except:
        flash('The reset password link is invalid or has expired.', 'danger')
        
    user = User.query.filter_by(email=email).first_or_404()
    flash('You have confirmed your account. You may now reset your password', 'success')
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():

        user.password = form.new_password.data
        db.session.add(user)
        db.session.commit()
        flash('Password reset successful, you may now login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset-password.html', title="Reset Password", form=form)
    
#unconfirmed
@auth.route('/unconfirmed')
#@login_required
def unconfirmed():
    if current_user.is_confirmed:
        #return redirect('home.mypage')
        return redirect('auth.login')
    flash('Please confirm your account!', 'warning')
    return render_template('auth/unconfirmed.html', title="Unconfirmed")
    
#register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(honors_id = form.honors_id.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    is_confirmed=False)
        db.session.add(user)
        db.session.commit()
        
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/activate.html', confirm_url=confirm_url)
        subject = "UMW Honors - Please confirm your email"
        send_email(user.email, subject, html)
        
        flash('You have successfully registered! Please check your email to confirm your account.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Create New Account')
    
        
#login 
@auth.route('/', methods=['GET', 'POST'])
def login():
    formLogin = LoginForm()
    dates = ImportantDate.query.all()
    
    if formLogin.validate_on_submit():
    
        user = User.query.filter_by(email=formLogin.email.data).first()
        if user is not None and user.verify_password(formLogin.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.mypage'))
        else:
            flash('Invalid email or password.')
    
    return render_template('home/index.html', formLogin=formLogin, title='Login', dates=dates)
    
#logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    
    return redirect(url_for('auth.login'))
      
#forgot password send email confirmation
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgotpassword():
    form = ResetPasswordEmailForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('auth.update_password', token=token, _external=True)
            html = render_template('auth/forgot-password-email.html', confirm_url=confirm_url)
            subject = "UMW Honors - Please confirm your email account."
            send_email(user.email, subject, html)
            flash('Please check your email for a reset link.')
        else: 
            flash('There is no account associated with that email address.', 'danger')
        
    return render_template('auth/forgot-password.html', form=form, title='Forgot Password')

    
#change password
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    user = current_user
    if form.validate_on_submit():
        if user.verify_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash('Password reset successful.', 'success')
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.mypage'))
        else: 
            flash('Old password field incorrect.', 'danger')
    
    return render_template('auth/change-password.html', form=form, title='Change Password')