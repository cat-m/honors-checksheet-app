from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, TextField, FileField, DateTimeField
from wtforms.validators import DataRequired


#file upload form for adding data to database
class FileUploadForm(FlaskForm):
    
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')
    
#file upload form for adding data to database
class StudentSearchForm(FlaskForm):
    
    studentID = TextField('Student Honors ID', validators=[DataRequired()])
    submit = SubmitField('Search')

#announcement upload form for adding announcement to database    
class AnnouncementForm(FlaskForm):
    
    title = TextField('Title', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
#form for adding dates to database
class DateForm(FlaskForm):
    
    title = TextField('Title', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')




