from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from forms import LoginForm, RegistrationForm, ResetPasswordForm, ChangePasswordForm
from .. import db
from ..models import User

#register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        user = User(honors_id = form.honors_id.data,
                    email=form.email.data,
                    first_name=form.last_name.data,
                    password=form.password.data)
                    
        db.session.add(user)
        db.session.commit()
        
        flash('You have successfully registered! You may now login.')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', form=form, title='Create New Account')
    
#login 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
            
        else:
            flash('Invalid email or password.')
    
    
    return render_template('auth/login.html', form=form, title='Login')
    
#logout
@auth.route('/logout')
@login_required
def logout():
    
    logout_user()
    flash('You have been logged out.')
    
    return redirect(url_for('auth.login'))
        
#forgot password
@auth.route('/forgot-password', methods=['GET', 'POST'])
def resetpassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_honorsID(form.honors_id.data):
            flash('Password reset successfully! Please check your email for your new password.')
            return redirect(url_for('auth.login'))
            
        else:
            flash('Invalid email or Honors ID.')
        
    return render_template('auth/login.html', form=form, title='Forgot Password')

#change password
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if user.verify_password(form.old_password.data):
            logout_user()
            flash('Password changed successfully! Please log in with your new password.')
            return redirect(url_for('auth.login'))
        else:
            flash('Password incorrect!')
        
    return render_template('auth/login.html', form=form, title='Change Password')