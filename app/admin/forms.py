from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, TextField, FileField
from wtforms.validators import DataRequired

#file upload form for adding data to database
class FileUploadForm(FlaskForm):
    
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')
    

    



