from flask import *
from database import *
import uuid
staff=Blueprint('staff',__name__)

@staff.route('/staff_home',methods=['get','post'])
def staff_home():
	if not session.get("lid") is None:
		data={}
		return render_template("staff_home.html",data=data)
	else:
		return redirect(url_for('public.login'))




@staff.route('/staff_View_assigned_class',methods=['get','post'])
def staff_View_assigned_class():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `assign_class` INNER JOIN `subject` USING (`subject_id`) INNER JOIN `class` USING (`class_id`) WHERE `staff_id`='%s'"%(session['id'])
		data['assign']=select(q)
		return render_template("staff_View_assigned_class.html",data=data)
	else:
		return redirect(url_for('public.login'))




@staff.route('/staff_Manage_students',methods=['get','post'])
def staff_Manage_students():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `staff` WHERE staff_id='%s'"%(session['id'])
		res2=select(q)
		id=res2[0]['department_id']
		q="SELECT * FROM `students` WHERE department_id='%s'"%(id)
		data['students']=select(q)
		if 'submit' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			
			gender=request.form['gender']
			
			
			
			phno=request.form['phno']
			email=request.form['email']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
			res=select(q)
			if res:
				flash('USER NAME ALREADY EXIST')
			else:
				q="INSERT INTO `login`(`username`,`password`,user_type)  VALUES ('%s','%s','student')"%(uname,pwd)
				lid=insert(q)
				q="INSERT INTO `students` (`login_id`,department_id,`first_name`,`last_name`,`gender`,`phone`,`email`) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(lid,id,fname,lname,gender,phno,email)
				insert(q)
				flash('REGISTERED')
				return redirect(url_for('staff.staff_Manage_students',id=id))
		if 'action' in request.args:
			action=request.args['action']
			did=request.args['did']
		else:
			action=None

		if action=='delete':
			q="DELETE FROM `students` WHERE `login_id`='%s'"%(did)
			delete(q)
			q="DELETE FROM `login` WHERE `login_id`='%s'"%(did)
			delete(q)
			flash('STUDENT DETAILS DELETED',id=id)
			return redirect(url_for('staff.staff_Manage_students',id=id))
		if action=='update':
			q="SELECT * FROM `students` WHERE `login_id`='%s'"%(did)
			data['student_up']=select(q)
		if 'updatez' in request.form:
			fname=request.form['fname']
			lname=request.form['lname']
			
			gender=request.form['gender']
			
			
			
			phno=request.form['phno']
			email=request.form['email']
			q="UPDATE `students` SET `first_name`='%s',`last_name`='%s',`gender`='%s',`phone`='%s',`email`='%s' WHERE `login_id`='%s'"%(fname,lname,gender,phno,email,did)
			
			update(q)
			flash('STUDENT DETAILS UPDATED')
			return redirect(url_for('staff.staff_Manage_students',id=id))
		return render_template("staff_Manage_students.html",data=data)
	else:
		return redirect(url_for('public.login'))




@staff.route('/staff_Schedule_Class',methods=['get','post'])
def staff_Schedule_Class():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `schedule_class` INNER JOIN `class` USING (`class_id`) WHERE `staff_id`='%s' ORDER BY `sh_class_id` DESC"%(session['id'])
		data['shedule']=select(q)
		q="SELECT * FROM `assign_class` INNER JOIN `class` USING (`class_id`) WHERE `staff_id`='%s'"%(session['id'])
		data['class']=select(q)
		if 'submit' in request.form:
			clas=request.form['clas']
			date=request.form['date']
			link=request.form['link']
			q="INSERT INTO `schedule_class` (`staff_id`,`class_id`,`date_time`,`video_link`) VALUES ('%s','%s','%s','%s')"%(session['id'],clas,date,link)
			insert(q)
			flash('CLASS ASSIGNED')
			return redirect(url_for('staff.staff_Schedule_Class'))
		if 'action' in request.args:
			action=request.args['action']
			did=request.args['did']
		else:
			action=None

		if action=='delete':
			q="DELETE FROM `schedule_class` WHERE `sh_class_id`='%s'"%(did)
			delete(q)
			
			flash('SHEDULE DETAILS DELETED')
			return redirect(url_for('staff.staff_Schedule_Class',id=id))
		return render_template("staff_Schedule_Class.html",data=data)
	else:
		return redirect(url_for('public.login'))




@staff.route('/staff_Create_video_link',methods=['get','post'])
def staff_Create_video_link():
	if not session.get("lid") is None:
		data={}
		return render_template("staff_Create_video_link.html",data=data)
	else:
		return redirect(url_for('public.login'))




@staff.route('/staff_View_Attendance',methods=['get','post'])
def staff_View_Attendance():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `attendance` INNER JOIN `schedule_class` USING (`sh_class_id`) INNER JOIN `class` USING (`class_id`) INNER JOIN `students` USING (`student_id`) WHERE `staff_id`='%s' ORDER BY `sh_class_id` DESC"%(session['id'])
		data['attendance']=select(q)
		return render_template("staff_View_Attendance.html",data=data)
	else:
		return redirect(url_for('public.login'))




# @staff.route('/staff_View_assigned_class',methods=['get','post'])
# def staff_View_assigned_class():
# 	if not session.get("lid") is None:
# 		data={}
# 		return render_template("staff_View_assigned_class.html",data=data)
# 	else:
# 		return redirect(url_for('public.login'))

