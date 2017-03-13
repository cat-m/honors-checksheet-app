from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, TextField, TextAreaField
from wtforms.validators import DataRequired, Email

#main contact form on contact us page
class ContactForm(FlaskForm):
    
    name = TextField('Name', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired(), Email()])
    phone = TextField('Phone')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    