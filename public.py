from flask import *
from database import *
import uuid
public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template("index.html")


@public.route('/login',methods=['get','post'])
def login():
	session.clear()
	if 'submit' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'"%(username,password)
		res=select(q)
		if not res:
			flash('INCORRECT USERNAME OR PASSWORD')
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['user_type']=='admin':
				flash('HELLO ADMIN')
				return redirect(url_for("admin.admin_home"))
			if res[0]['user_type']=='staff':
				q="SELECT * FROM `staff` WHERE `login_id`='%s'"%(res[0]['login_id'])
				re=select(q)
				if re:
					session['id']=re[0]['staff_id']
					flash('HELLO STAFF')
					return redirect(url_for("staff.staff_home"))

	return render_template("login.html")



