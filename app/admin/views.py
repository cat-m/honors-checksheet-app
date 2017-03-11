from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from . import admin
from forms import FileUploadForm
from .. import db
from ..models import User

#file upload
@admin.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    
    form = FileUploadForm()
    
    if form.validate_on_submit():
        flash('Upload Successful!')
        return redirect(url_for('admin.upload'))
        
    return render_template('admin/upload.html', title="Upload File", form=form)