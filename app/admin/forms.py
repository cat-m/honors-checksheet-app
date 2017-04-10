from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, TextField, FileField
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
    date_time = TextField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Announcement')



