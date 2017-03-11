from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

#register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        user = User(honors_id = form.honors_id.data,
                    email=form.email.data,
                    username=form.username.data,
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
            
            return redirect(url_for('home.dashboard_student'))
            
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