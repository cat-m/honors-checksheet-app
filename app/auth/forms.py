from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User

#student registration form
class RegistrationForm(FlaskForm):
    
    honors_id = StringField('Honors ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), 
                                            EqualTo('confirm_password')
                                            ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')
    
    #check to see if the email address is already in the database
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')
    
    #check to see if the username is already in the database
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')
   
#login form on login page         
class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Form for User to reset forgotten password    
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    honors_id = StringField('Honors ID', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    
# Form for User to change password from their account
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')