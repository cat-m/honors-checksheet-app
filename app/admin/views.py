from flask import flash, redirect, request, render_template, url_for, abort
from flask_login import login_required, current_user
from flask_sqlalchemy import sqlalchemy
import datetime
from sqlalchemy import text
from werkzeug.utils import secure_filename
import pandas as pd
import csv


from . import admin
from forms import FileUploadForm, StudentSearchIDForm, StudentSearchNameForm, AnnouncementForm, DateForm
from .. import db
from ..models import User, Checksheet, Announcement, ImportantDate

    
#file upload
@admin.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    dates = ImportantDate.query.order_by(ImportantDate.date_time)
    if not current_user.is_admin:
        #throw a 403 error. we could do a custom error page later.
        abort(403)
    formUpload = FileUploadForm()
    if formUpload.validate_on_submit():
        if 'file' not in request.files:
            flash('No File')
            return redirect(request.url)
        file = request.files['file']
        try:
            num_rows_deleted = db.session.query(Checksheet).delete()
            db.session.commit()
            flash('Checksheet database successfully dumped', 'success')
        except:
            db.session.rollback()
            flash('There was an error dumping the Checksheet database', 'danger')
            
        try:
            parse_dates = ['Initial essay', 'Date 1', 'Date 2', 'Date 3', 'Date 4', 'Date 5', 'Date 6', 'Date 7', 'Date 8']
            checksheet = pd.read_csv(file, parse_dates=parse_dates)
            checksheet.dropna(axis=0, how='all', inplace=True)
            checksheet.columns = ['lastName', 'firstName', 'honors_id', 'email', 'admitted', 'dupontCode', 'status', 'comments', 'term', 'major', 'advisor', 'initialEssayDate', 'coCur1', 'coCurDate1', 'coCur2', 'coCurDate2', 'coCur3', 'coCurDate3', 'coCur4', 'coCurDate4', 'coCur5', 'coCurDate5', 'coCur6', 'coCurDate6', 'coCur7', 'coCurDate7', 'coCur8', 'coCurDate8', 'fsemHN', 'fsemHNDate', 'hnCourse1', 'hnCourse1Date', 'hnCourse2', 'hnCourse2Date', 'hnCourse3', 'hnCourse3Date', 'hnCourse4', 'hnCourse4Date', 'hnCourse5', 'hnCourse5Date', 'researchCourse', 'researchCourseDate', 'capstoneCourse', 'capstoneCourseDate', 'hon201', 'hon201Date', 'leadership', 'mentoring', 'portfolio4', 'portfolio1', 'portfolio2', 'portfolio3', 'exit']
            checksheet.to_sql('checksheets', con=db.engine, if_exists='append', index=False)
            flash('Upload Successful!')
            print checksheet['coCurDate1']
            
            # drop old users from database
            try:
                students = User.query.filter_by(is_admin=0).all()
                if students is not None:
                    for student in students:
                        print("student=%s" % student.username)
                        try:
                            found = Checksheet.query.filter_by(honors_id=student.honors_id).first()
                            print(found)
                            if found is None:
                                try:
                                    user = User.query.get_or_404(student.id)
                                    db.session.delete(user)
                                    db.session.commit()
                                except:
                                    db.session.rollback()
                                    flash('User not deleted','danger')
                        except:
                            flash('Error when searching Checksheet table','danger')
                else:
                    flash('There are currently no student accounts.','warning')
            except:
                flash('Error searching Users table','danger')
        except: 
            flash('The file you uploaded has an error. Please check the format and try again.')

        return redirect(url_for('admin.upload'))
        
    return render_template('admin/upload.html', title="Upload", formUpload=formUpload, dates=dates)
    
    
#search for student
@admin.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    dates = ImportantDate.query.order_by(ImportantDate.date_time)
    if not current_user.is_admin:
        #throw a 403 error. we could do a custom error page later.
        abort(403)
    formSearch = StudentSearchIDForm()
    formNameSearch = StudentSearchNameForm()
    if formSearch.validate_on_submit():
        student_honors_id = formSearch.studentID.data
        student_checksheet = Checksheet.query.filter_by(honors_id=student_honors_id).first()
        title = "%s's Checksheet" % student_checksheet.firstName #student_honors_id
 
        return render_template('home/view-checksheet.html', title=title, checksheet=student_checksheet)
        
    if formNameSearch.validate_on_submit():
        student_name = formNameSearch.studentName.data
        student_results = Checksheet.query.filter(Checksheet.lastName.like("%"+student_name+"%")).all()

        return render_template('home/view-search-results.html', title="Search Results", results=student_results)

    return render_template('admin/search.html', title="Search", formSearch=formSearch, formNameSearch=formNameSearch, dates=dates)

#display student checksheet after search
@admin.route('/checksheet-result/<int:honorsid>', methods=['GET', 'POST'])
@login_required
def view_student_checksheet(honorsid):
    if not current_user.is_admin:
        abort(403)
    
    student_checksheet = Checksheet.query.filter_by(honors_id=honorsid).first_or_404()
    title = "%s's Checksheet" % student_checksheet.firstName #honorsid
    
    return render_template('home/view-checksheet.html', checksheet=student_checksheet, title=title)
    
#add an announcement
@admin.route('/announcement/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    dates = ImportantDate.query.order_by(ImportantDate.date_time)
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
        return redirect(url_for('home.admin_dashboard'))
        
    return render_template('admin/announcement.html', title="Add Announcement", action="Add", add_announcement=add_announcement, form=form, dates=dates)


#edit an announcement
@admin.route('/announcement/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    if not current_user.is_admin:
        abort(403)
        
    add_announcement = False
    dates = ImportantDate.query.order_by(ImportantDate.date_time)
    
    announcement = Announcement.query.get_or_404(id)
    form = AnnouncementForm(obj=announcement)
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.description = form.description.data
        db.session.commit()
        flash('You have sucessfully edited the announcement.', 'success')
        return redirect(url_for('home.admin_dashboard'))
        
    form.title.data = announcement.title
    form.description.data = announcement.description
    
    return render_template('admin/announcement.html', title="Edit Announcement", action="Edit", add_announcement=add_announcement, form=form, announcement=announcement, dates=dates)
        
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

#add an important date
@admin.route('/date/add', methods=['GET', 'POST'])
@login_required
def add_date():
    if not current_user.is_admin:
        #throw a 403 error if the user is not an admin user
        abort(403)
    add_date = True
    dates = ImportantDate.query.order_by(ImportantDate.date_time)
        
    form = DateForm()
    if form.validate_on_submit():
        newDate = ImportantDate(title=form.title.data,
                    info=form.info.data,
                    date_time=form.date.data)
        db.session.add(newDate)
        db.session.commit()
        flash('Date successfully added!', 'success')
        return redirect(url_for('home.admin_dashboard'))
        
#    if request.method=="POST":
#        form=request.form
#        newDate = ImportantDate(title=form['title'],info=form['info'],date_time=form['date'])
#        db.session.add(newDate)
#        db.session.commit()
#        flash('Date successfully added!', 'success')
#        return redirect(url_for('home.admin_dashboard'))
        
    return render_template('admin/edit-dates.html', title="Add Date", action="Add", add_date=add_date, form=form, dates=dates)    

#edit an important date
@admin.route('/date/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_date(id):
    if not current_user.is_admin:
        #throw a 403 error if the user is not an admin user
        abort(403)
        
    add_date = False
    dates = ImportantDate.query.order_by(ImportantDate.date_time)
    
    date = ImportantDate.query.get_or_404(id)
    form = DateForm(obj=date)
    if form.validate_on_submit():
        date.title = form.title.data
        date.info = form.info.data
        date.date_time=form.date.data
        db.session.commit()
        flash('You have sucessfully edited the date.', 'success')
        return redirect(url_for('home.admin_dashboard'))
        
    form.title.data = date.title
    form.info.data = date.info
    form.date.data = date.date_time
    
    return render_template('admin/edit-dates.html', title="Edit Date", action="Edit", add_date=add_date, form=form, date=date, dates=dates)
        
#delete an important date
@admin.route('/date/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_date(id):
    if not current_user.is_admin:
        #throw a 403 error if the user is not an admin user
        abort(403)
    
    date = ImportantDate.query.get_or_404(id)
    db.session.delete(date)
    db.session.commit()
    flash('You have successfully deleted the date.', 'success')
    
    return redirect(url_for('home.admin_dashboard'))
