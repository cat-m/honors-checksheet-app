from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, TextField, TextAreaField, PasswordField, ValidationError, StringField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Email, EqualTo


#main contact form on contact us page
class ContactForm(FlaskForm):
    
    name = TextField('Name', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
#login form on login page         
class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')