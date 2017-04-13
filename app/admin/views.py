from flask import flash, redirect, request, render_template, url_for, abort
from flask_login import login_required, current_user
from flask_sqlalchemy import sqlalchemy
import datetime
from sqlalchemy import text
from werkzeug.utils import secure_filename
import pandas as pd
import csv


from . import admin
<<<<<<< HEAD
from forms import FileUploadForm, StudentSearchForm, AddAnnouncementForm, AddDateForm
=======
from forms import FileUploadForm, StudentSearchForm, AnnouncementForm
>>>>>>> 64c7f01a2054a266b0f81cfa8beaebcc9ca19d55
from .. import db
from ..models import User, Checksheet, Announcement, ImportantDate

    
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
        file = request.files['file']
        try:
            checksheet = pd.read_csv(file)
            checksheet.columns = ['firstName', 'lastName', 'honors_id', 'email', 'admitted', 'dupontCode', 'status', 'comments', 'term', 'major', 'advisor', 'initialEssayDate', 'coCur1', 'coCurDate1', 'coCur2', 'coCurDate2', 'coCur3', 'coCurDate3', 'coCur4', 'coCurDate4', 'coCur5', 'coCurDate5', 'coCur6', 'coCurDate6', 'coCur7', 'coCurDate7', 'coCur8', 'coCurDate8', 'fsemHN', 'fsemHNDate', 'hnCourse1', 'hnCourse1Date', 'hnCourse2', 'hnCourse2Date', 'hnCourse3', 'hnCourse3Date', 'hnCourse4', 'hnCourse4Date', 'hnCourse5', 'hnCourse5Date', 'researchCourse', 'researchCourseDate', 'capstoneCourse', 'capstoneCourseDate', 'hon201', 'hon201Date', 'leadership', 'mentoring', 'portfolio4', 'portfolio1', 'portfolio2', 'portfolio3', 'exit']
            checksheet.to_sql('checksheets', con=db.engine, if_exists='append', index=False)
            flash('Upload Successful!')
        except: 
            flash('The file you uploaded has an error. Please check the format and try again.')

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
        student_honors_id = formSearch.studentID.data
        student_checksheet = Checksheet.query.filter_by(honors_id=student_honors_id).first()
        title = "Student %s's Checksheet" % student_honors_id
 
        return render_template('home/view-checksheet.html', title=title, checksheet=student_checksheet)
        
        #return redirect(url_for('admin.checksheet'))
        
    return render_template('admin/search.html', title="Search", formSearch=formSearch)

@admin.route('/announcement/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    if not current_user.is_admin:
        #throw a 403 error. we could do a custom error page later.
        abort(403)
    add_announcement = True
    
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data,
                    description=form.description.data,
                    created=datetime.datetime.now())
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement successfully added!', 'success')
        
    return render_template('admin/announcement.html', title="Add Announcement", action="Add", add_announcement=add_announcement, form=form)



@admin.route('/edit-dates', methods=['GET', 'POST'])
@login_required
def editDates():
    if not current_user.is_admin:
        #throw a 403 error. we could do a custom error page later.
        abort(403)
    addDate = AddDateForm()
    if addDate.validate_on_submit():
        date = ImportantDate(title=addDate.title.data,
                    description=addDate.description.data,
                    date=addDate.date.data)
        db.session.add(date)
        db.session.commit()
    return render_template('admin/edit-dates.html', title="EditDates", addDate=addDate)


#edit an announcement
@admin.route('/announcement/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    if not current_user.is_admin:
        abort(403)
        
    add_announcement = False
    
    announcement = Announcement.query.get_or_404(id)
    form = AnnouncementForm(obj=announcement)
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.description = form.description.data
        db.session.commit()
        flash('You have sucessfully edited the announcement.', 'success')
    
        
    form.title.data = announcement.title
    form.description.data = announcement.description
    
    return render_template('admin/announcement.html', title="Edit Announcement", action="Edit", add_announcement=add_announcement, form=form, announcement=announcement)
        
#delete an announcement
@admin.route('/announcement/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_announcement(id):
    if not current_user.is_admin:
        abort(403)
    
    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    flash('You have successfully deleted the announcement.', 'success')
    
    return redirect(url_for('home.admin_dashboard'))
    
    
#route to student's checksheet
@admin.route('/checksheet', methods=['GET','POST'])
@login_required
#@check_confirmed
def checksheet():
    student_honors_id = current_user.honors_id
    student_checksheet = Checksheet.query.filter_by(honors_id=student_honors_id).first()
   
    return render_template('home/view-checksheet.html', title="Student's Checksheet", checksheet=student_checksheet)

