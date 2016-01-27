# -*- coding: utf-8 -*-
from Dtoy import app
from flask.views import MethodView
from flask import render_template, flash,url_for, redirect,g,jsonify,request,abort
from models import User,db
from forms import LoginForm,UseraddForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from functools import wraps
logined = []


def  manager_requested(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		identity = g.user.identity
		identity = identity.encode('utf-8')
		manager = u'管理员'.encode('utf-8')
		if identity == manager:
			return f(*args, **kwargs)
		return abort(403)
	return decorated_function


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('error/403.html'), 403


class Home_View(MethodView):

	decorators = [login_required]

	def get(self):
		return render_template('home.html')


class User_View(MethodView):
	
	decorators = [login_required]

	def get(self,username):
		if username is None:
			return render_template('home.html')
		else:
			user = User.query.filter_by(uid=1).first()
			return jsonify(result=user.nickname)


class Login_View(MethodView):

	def get(self):
		if g.user is not None and g.user.is_authenticated:
			return redirect(url_for('home'))
		else:
			form = LoginForm()
			return render_template('user/login.html',form=form)

	def post(self):


		form = LoginForm()
		if form.validate() == False:
				return render_template('user/login.html', form=form)
		else:
			remember_me = False
			user = User.query.filter_by(email = form.email.data).first()

			login_user(user, remember = remember_me)

			logined.append(g.user)
			app.logger.info('%s use %s login.',request.remote_addr,g.user)

			# nexturl = request.referrer
			# tmp = nexturl.split('next=')[1]
			# nexturl = tmp.replace('%2F','/')
			return redirect(url_for('deploy/deploy'))
			# return redirect(url_for(request.args.get('next')) or url_for('user'))

class Logout_View(MethodView):

	def get(self):
		logout_user()
		return redirect(url_for('home'))


class UserAdd_View(MethodView):

	decorators = [login_required,manager_requested]

	def get(self):
		form = UseraddForm()
		return render_template('user/useradd.html',form=form)

	def post(self):
		form = UseraddForm()

		if form.validate() == False:
			return render_template('user/useradd.html', form=form)
		else:
			newuser = User(form.nickname.data, form.username.data,form.identity.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			app.logger.info('Manager:%s add user :%s.',g.user,newuser)

			return redirect(url_for('user'))

class UserManage_View(MethodView):

	decorators = [login_required,manager_requested]

	def get(self):
		userlist = User.query.filter_by().order_by(User.nickname) 
		return render_template('user/usermanager.html',userlist=userlist)

	def post(self):
		uid = request.form['uid']

		try:
			user = User.query.filter_by(uid = uid).first()
			db.session.delete(user)
			db.session.commit()

			app.logger.info('Manager:%s delete user :%s.',g.user,user)

			return jsonify(result='成功移除')

		except:
			return jsonify(result='user is not exist')

class UserProfile_View(MethodView):

	decorators = [login_required]

	def get(self):
		return render_template('user/profile.html')