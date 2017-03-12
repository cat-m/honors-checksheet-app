from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from . import admin
from forms import FileUploadForm, StudentSearchForm
from .. import db
from ..models import User

#file upload
@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    
    formUpload = FileUploadForm()
    formSearch = StudentSearchForm()
    
    if formUpload.validate_on_submit():
        flash('Upload Successful!')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/dashboard.html', title="Dashboard", formUpload=formUpload, formSearch=formSearch)