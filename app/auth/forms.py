from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User
from ..models import Checksheet

#student registration form
class RegistrationForm(FlaskForm):
    
    honors_id = StringField('Honors ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')
    
    #check to see if the honors_id is in the checksheets table. if no, error.
    #check to see if the honors_id is already in use with another account in the database. if yes, error.
    def validate_honors_id(self, field):
        honors = Checksheet.query.filter_by(honors_id=field.data).first()
        if honors is None:
            raise ValidationError('That Honors ID is not in the database. Please check your Honors ID and try again.')
        if User.query.filter_by(honors_id=field.data).first():
            raise ValidationError('An account has already been made for the student with this Honors ID number.')

    #check to see if the email address is already listed in the database with another user. if yes, error.
    #check to see if email address is listed with a student row in the checksheets table. if no, error.
    def validate_email(self, field):
        result = Checksheet.query.filter_by(email=field.data).first()
        if result is None or result.honors_id != self.honors_id.data:
            raise ValidationError('This email address does not match our records. Please double-check your Honors ID and use your UMW email address.')
        #print("HEY LOOK AT THIS PRINT STATEMENT: honors_id = %s, result.honors_id = %s" % (self.honors_id.data,result.honors_id))
        
        
# Login form on index page (login page)        
class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Form for logged in User to change password
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password1 = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
   
# Form for user to request a reset of a forgotten password 
class ResetPasswordEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')
    
# Form for User to request a password change if they have forgotten
class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    
    