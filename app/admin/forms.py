from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, TextField, FileField, DateField
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
class AddAnnouncementForm(FlaskForm):
    
    title = TextField('Title', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
    date = TextField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Announcement')
    
#form for adding dates to database
class AddDateForm(FlaskForm):
    
    title = TextField('Title', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Date')



