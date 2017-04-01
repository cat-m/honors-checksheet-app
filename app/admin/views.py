from flask import flash, redirect, request, render_template, url_for, abort
from flask_login import login_required, current_user
from flask.ext import excel
from flask_sqlalchemy import sqlalchemy
from werkzeug.utils import secure_filename
import pandas as pd


from . import admin
from forms import FileUploadForm, StudentSearchForm
from .. import db
from ..models import User, Checksheet


#file upload
@admin.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if not current_user.is_admin:
        #throw a 403 error. we could do a custom error page later.
        abort(403)
    formUpload = FileUploadForm()
    if formUpload.validate_on_submit():
        checksheet = pd.read_csv('file')
        checksheet.to_sql(name='checksheets', if_exist='append', db=db)
        flash('Upload Successful!')
        return redirect(url_for('admin.upload'))
        
    return render_template('admin/upload.html', title="Upload", formUpload=formUpload)
    
    
#search for student
@admin.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if not current_user.is_admin:
        #throw a 403 error. we could do a custom error page later.
        abort(403)
    formSearch = StudentSearchForm()
    if formSearch.validate_on_submit():
        return redirect(url_for('admin.search'))
        
    return render_template('admin/search.html', title="Search", formSearch=formSearch)
    