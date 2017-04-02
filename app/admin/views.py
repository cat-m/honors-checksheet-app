from flask import flash, redirect, request, render_template, url_for, abort
from flask_login import login_required, current_user
from flask.ext import excel
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import text
from werkzeug.utils import secure_filename
import pandas as pd
import csv


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
        if 'file' not in request.files:
            flash('no file part')
            return redirect(request.url)
        file = request.files['file'].read()
        checksheet = pd.read_csv(file, error_bad_lines=False)

        for row in checksheet:
            print(row)
        
        
        sql = text("INSERT INTO 'checksheets' ('lastName', 'firstName', 'honors_id', 'email', 'admitted', 'dupontCode', 'status', 'comments', 'term', 'coCur1', 'coCurDate1', 'coCur2', 'coCurDate2', 'coCur3', 'coCurDate3', 'coCur4', 'coCurDate4', 'coCur5', 'coCurDate5', 'coCur6', 'coCurDate6', 'coCur7', 'coCurDate7', 'coCur8', 'coCurDate8', 'fsemHN', 'fsemHNDate', 'hnCourse1', 'hnCourse1Date', 'hnCourse2', 'hnCourse2Date', 'hnCourse3', 'hnCourse3Date', 'hnCourse4', 'hnCourse4Date', 'hnCourse5', 'hnCourse5Date', 'researchCourse', 'researchCourseDate', 'capstoneCourse', 'capstoneCourseDate', 'hon201', 'hon201Date', 'leadership', 'mentoring', 'portfolio4', 'portfolio1', 'portfolio2', 'portfolio3', 'exit') VALUES ('?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?');")
        result = db.engine.execute(sql)
        for row in result:
            ourData.append(row)
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
    