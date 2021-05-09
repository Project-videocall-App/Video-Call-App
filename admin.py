from flask import *
from database import *
import uuid
admin=Blueprint('admin',__name__)

@admin.route('/admin_home',methods=['get','post'])
def admin_home():
	if not session.get("lid") is None:
		data={}
		return render_template("admin_home.html",data=data)
	else:
		return redirect(url_for('public.login'))




@admin.route('/admin_Manage_staff',methods=['get','post'])
def admin_Manage_staff():
	if not session.get("lid") is None:
		data={}
		id=request.args['id']
		data['id']=id
		q="SELECT * FROM `staff` WHERE department_id='%s'"%(id)
		data['staff']=select(q)
		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			
			gender=request.form['gender']
			
			qua=request.form['qua']
			
			phno=request.form['phno']
			email=request.form['email']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
			res=select(q)
			if res:
				flash('USER NAME ALREADY EXIST')
			else:
				q="INSERT INTO `login`(`username`,`password`,user_type)  VALUES ('%s','%s','staff')"%(uname,pwd)
				lid=insert(q)
				q="INSERT INTO `staff` (`login_id`,department_id,`first_name`,`last_name`,`gender`,`qualification`,`phone`,`email`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(lid,id,fname,lname,gender,qua,phno,email)
				insert(q)
				flash('REGISTERED')
				return redirect(url_for('admin.admin_Manage_staff',id=id))
		if 'action' in request.args:
			action=request.args['action']
			did=request.args['did']
		else:
			action=None

		if action=='delete':
			q="DELETE FROM `staff` WHERE `login_id`='%s'"%(did)
			delete(q)
			q="DELETE FROM `login` WHERE `login_id`='%s'"%(did)
			delete(q)
			flash('STAFF DETAILS DELETED',id=id)
			return redirect(url_for('admin.admin_Manage_staff',id=id))
		if action=='update':
			q="SELECT * FROM `staff` WHERE `login_id`='%s'"%(did)
			data['staff_up']=select(q)
		if 'updatez' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			
			gender=request.form['gender']
			
			qua=request.form['qua']
			
			phno=request.form['phno']
			email=request.form['email']
			q="UPDATE `staff` SET `first_name`='%s',`last_name`='%s',`gender`='%s',`qualification`='%s',`phone`='%s',`email`='%s' WHERE `login_id`='%s'"%(fname,lname,gender,qua,phno,email,did)
			
			update(q)
			flash('STAFF DETAILS UPDATED')
			return redirect(url_for('admin.admin_Manage_staff',id=id))
		return render_template("admin_Manage_staff.html",data=data)
	else:
		return redirect(url_for('public.login'))






@admin.route('/admin_Manage_department',methods=['get','post'])
def admin_Manage_department():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `department` ORDER BY `department_id` DESC"
		data['department']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None

		if action=='delete':
			q="DELETE FROM `department` WHERE `department_id`='%s'"%(id)
			delete(q)
			flash('DEPARTMENT DETAILS DELETED')
			return redirect(url_for('admin.admin_Manage_department'))
		if 'submit' in request.form:
			dep=request.form['dep']
			q="INSERT INTO `department` (`department`) VALUES ('%s')"%(dep)
			insert(q)
			flash('DEPARTMENT DETAILS ADDED')
			return redirect(url_for('admin.admin_Manage_department'))
		return render_template("admin_Manage_department.html",data=data)
	else:
		return redirect(url_for('public.login'))






@admin.route('/admin_Manage_Subject',methods=['get','post'])
def admin_Manage_Subject():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `subject` ORDER BY `subject_id` DESC"
		data['sub']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None

		if action=='delete':
			q="DELETE FROM `subject` WHERE `subject_id`='%s'"%(id)
			delete(q)
			flash('SUBJECT DETAILS DELETED')
			return redirect(url_for('admin.admin_Manage_Subject'))
		if 'submit' in request.form:
			dep=request.form['dep']
			q="INSERT INTO `subject` (`subject_name`) VALUES ('%s')"%(dep)
			insert(q)
			flash('SUBJECT DETAILS ADDED')
			return redirect(url_for('admin.admin_Manage_Subject'))
		return render_template("admin_Manage_Subject.html",data=data)
	else:
		return redirect(url_for('public.login'))






@admin.route('/admin_Manage_class',methods=['get','post'])
def admin_Manage_class():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `class` INNER JOIN `department` USING (`department_id`) ORDER BY `department_id` DESC"
		data['class']=select(q)
		q="SELECT * FROM `department` ORDER BY `department_id` DESC"
		data['department']=select(q)
		if 'submit' in request.form:
			dep=request.form['dep']
			classs=request.form['class']
			q="INSERT INTO `class` (`department_id`,`class`) VALUES ('%s','%s')"%(dep,classs)
			insert(q)
			flash('CLASS DETAILS ADDED')
			return redirect(url_for('admin.admin_Manage_class'))
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None

		if action=='delete':
			q="DELETE FROM `class` WHERE `class_id`='%s'"%(id)
			delete(q)
			flash('CLASS DETAILS DELETED')
			return redirect(url_for('admin.admin_Manage_class'))
		return render_template("admin_Manage_class.html",data=data)
	else:
		return redirect(url_for('public.login'))






@admin.route('/admin_Assign_class_and_subject_for_staff',methods=['get','post'])
def admin_Assign_class_and_subject_for_staff():
	if not session.get("lid") is None:
		data={}
		id=request.args['id']
		data['id']=id
		q="SELECT * FROM `assign_class` INNER JOIN `subject` USING (`subject_id`) INNER JOIN `staff` USING (`staff_id`) WHERE `class_id`='%s'"%(id)
		data['assign']=select(q)
		
		q="SELECT * FROM `class` INNER JOIN `department` USING (`department_id`) WHERE class_id='%s'"%(id)
		data['class']=select(q)
		q="SELECT * FROM `subject`"
		data['sub']=select(q)
		q="SELECT * FROM `staff` WHERE `department_id`='%s'"%(id)
		data['staff']=select(q)
		if 'submit' in request.form:
			sub=request.form['sub']
			staff=request.form['staff']
			q="SELECT * FROM `assign_class` WHERE `staff_id`='%s' AND `subject_id`='%s'"%(staff,sub)
			res=select(q)
			if res:
				flash('ALREADY ASSIGNED')
				return redirect(url_for('admin.admin_Assign_class_and_subject_for_staff',id=id))
			else:
				q="INSERT INTO `assign_class` (`class_id`,`staff_id`,`subject_id`) VALUES ('%s','%s','%s')"%(id,staff,sub)
				insert(q)
				flash('ASSIGNED')
				return redirect(url_for('admin.admin_Assign_class_and_subject_for_staff',id=id))
		return render_template("admin_Assign_class_and_subject_for_staff.html",data=data)
	else:
		return redirect(url_for('public.login'))






@admin.route('/admin_View_students',methods=['get','post'])
def admin_View_students():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `students` INNER JOIN `department` USING (`department_id`) ORDER BY department_id DESC"
		data['student']=select(q)
		return render_template("admin_View_students.html",data=data)
	else:
		return redirect(url_for('public.login'))





