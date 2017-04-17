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
class AnnouncementForm(FlaskForm):
    
    title = TextField('Title', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
<<<<<<< HEAD
    submit = SubmitField('Add Announcement')
=======
    submit = SubmitField('Submit')
    
#form for adding dates to database
class DateForm(FlaskForm):
    
    title = TextField('Title', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

>>>>>>> ea5d48543b2683a433dffa9edcc4062454983340



