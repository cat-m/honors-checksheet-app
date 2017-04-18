from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, TextField, FileField, DateField
from wtforms.validators import DataRequired


#file upload form for adding data to database
class FileUploadForm(FlaskForm):
    
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')
    
#search for student by Honors_ID
class StudentSearchIDForm(FlaskForm):
    
    studentID = TextField('Student Honors ID', validators=[DataRequired()])
    submit = SubmitField('Search')

#search for stucent by Name
class StudentSearchNameForm(FlaskForm):
    
    studentName= TextField('Student Name', validators=[DataRequired()])
    submit = SubmitField('Search')

#announcement upload form for adding announcement to database    
class AnnouncementForm(FlaskForm):
    
    title = TextField('Title', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
#form for adding dates to database
class DateForm(FlaskForm):
    
    title = TextField('Title', validators=[DataRequired()])
    info = TextField('Info', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')




