from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from . import admin
from forms import FileUploadForm, StudentSearchForm
from .. import db
from ..models import User


#file upload
@admin.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    
    formUpload = FileUploadForm()

    
    if formUpload.validate_on_submit():
        flash('Upload Successful!')
        return redirect(url_for('home.admin_dashboard'))
        
    return render_template('admin/upload.html', title="Upload", formUpload=formUpload)
    
#search for student
@admin.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    
    formSearch = StudentSearchForm()

    
    if formSearch.validate_on_submit():
        
        return redirect(url_for('home.admin_dashboard'))
        
    return render_template('admin/search.html', title="Search", formSearch=formSearch)
    