# -*- coding: utf-8 -*-
from Dtoy import app,db,socketio
from Dtoy.user.UserView import manager_requested
from flask.views import MethodView
from flask import render_template,redirect,g,url_for,request,jsonify
from flask.ext.login import login_required
from forms import AppInfoForm,DeployForm
from models import AppInfoDB,DeployLogDB
import subprocess,re
from sqlalchemy import desc


from flask_socketio import  emit
import time
from datetime import datetime


class Deploy_View(MethodView):

	decorators = [login_required]

	def get(self):
		appinfolist = AppInfoDB.query.filter_by().order_by() 
		return render_template('deploy/deploy.html',appinfolist=appinfolist)

	def post(self):
		appname = request.form['appname']
		branch = request.form['branch']
		socketresponse = request.form['socketresponse']

	
		appinfolist = AppInfoDB.query.filter_by(appname=appname).first() 
		apptype = appinfolist.apptype
		path = '/web/code/eln4-git/' + apptype + '/' + appname
		path2 = '/web/code/eln4-git/' + apptype + '/app-' + appname

		socketio.emit(socketresponse,
			{'data': u'开始发布', 'time': time.ctime()},
			namespace='/websocket/runlog')


		pathshell = 'if [ -d ' + path2 + ' ] ; then echo ' + path2 + ';elif [ -d ' + path + ' ] ;then echo '+ path + ' ;else echo no;fi'

		p = subprocess.Popen(pathshell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			print line

		if line == 'no':
			socketio.emit(socketresponse,
				{'data': u'应用不存在，请添加', 'time': time.ctime()},
				namespace='/websocket/runlog')
			return jsonify(result='应用不存在，请添加')

		else:
			path = line.strip('\n')

		socketio.emit(socketresponse,
			{'data': u'应用确认完毕，开始更新代码', 'time': time.ctime()},
			namespace='/websocket/runlog')

		# app.logger.info('Now path is %s',path)

		gitshell = 'cd ' + path + '; git pull ; git checkout ' + branch 
		mvnshell = 'cd ' + path + '; mvn clean deploy  -DskipTests '

		# app.logger.info('gitshell is %s',gitshell)

		p = subprocess.Popen(gitshell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		while p.poll() == None:
			line = p.stdout.readline()
			print line
			socketio.emit(socketresponse,
				{'data':line, 'time': time.ctime()},
				namespace='/websocket/runlog')

		gitresult = p.wait()
		if gitresult != 0:
			return jsonify(result='git 更新代码失败')

		socketio.emit(socketresponse,
			{'data': u'git代码更新成功，开始编译', 'time': time.ctime()},
			namespace='/websocket/runlog')

		p = subprocess.Popen(mvnshell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	
		while p.poll() == None:
			line = p.stdout.readline()
			print line
			line = re.sub(r"(\d+)/(\d+)\sKB",'',line)
			socketio.emit(socketresponse,
				{'data':line.strip(), 'time': time.ctime()},
				namespace='/websocket/runlog')

		mvnresult = p.wait()

		if mvnresult == 0:
			app.logger.info('User %s deploy app %s done!',g.user,appname)
			result = u'打包成功'
			user = str(g.user)
			submit_time = datetime.now()
			deploylog = DeployLogDB(appname,user,result,submit_time)
			db.session.add(deploylog)
			db.session.commit()

			return jsonify(result=result)
		else:
			return jsonify(result='mvn编译发布失败')



class AppInfoAdd_View(MethodView):

	decorators = [login_required,manager_requested]

	def get(self):
		form = AppInfoForm()
		appinfolist = AppInfoDB.query.filter_by().order_by() 
		return render_template('deploy/appinfoadd.html',form=form,appinfolist=appinfolist)


	def post(self):
		form = AppInfoForm()

		if form.validate() == False:
			return render_template('deploy/appinfoadd.html', form=form)
		else:
			submitter = str(g.user)
			# app.logger.info('appname is %s',form.appname.data)
			giturl = 'ssh://git@gitlab.21tb.com:4350/eln/' + form.apptype.data + '-' + form.appname.data + '.git'
			appinfo = AppInfoDB(form.appname.data, form.apptype.data,giturl,form.branch.data, form.typeinfo.data, submitter,form.remarks.data)
			db.session.add(appinfo)
			db.session.commit()


			return redirect(url_for('deploy/appinfomanager'))


class AppInfoManager_View(MethodView):

	decorators = [login_required,manager_requested]

	def get(self):
		appinfolist = AppInfoDB.query.filter_by().order_by() 
		return render_template('deploy/appinfomanager.html',appinfolist=appinfolist)


	def post(self):
		uid = request.form['uid']

		try:
			appinfo = AppInfoDB.query.filter_by(uid = uid).first()
			db.session.delete(appinfo)
			db.session.commit()

			app.logger.info('Manager:%s delete appinfo :%s.',g.user,appinfo.appname)

			return jsonify(result='成功移除')

		except:
			return jsonify(result='app is not exist')


class Branch_View(MethodView):
	"""docstring for Branch_View"""

	decorators = [login_required]

	def post(self):
		appname = request.form['appname']
		if appname:
			appinfo = AppInfoDB.query.filter_by(appname = appname).first()
		# app.logger.info('appname is %s',appname)
		# return jsonify(result='ok')
			return jsonify(result=appinfo.branch)
		else:
			return jsonify(result='')


class DeployLog_View(MethodView):

	decorators = [login_required]

	def get(self):
		# deployloglist = DeployLogDB.query.filter_by().order_by(desc('id')).offset(0).limit(10) 
		# deployloglist = DeployLogDB.query.filter_by().order_by(desc('id'))
		return render_template('deploy/deploylog.html')


	def post(self):
		deploylogdict = {}
		appname = request.form['appname']
		user = request.form['user']
		start_time = request.form['start_time']
		end_time = request.form['end_time']


		if start_time  and end_time:
			start_time = datetime.strptime(start_time,'%Y-%m-%d')
			end_time = datetime.strptime(end_time,'%Y-%m-%d')
			deployloglist = DeployLogDB.query.filter(DeployLogDB.appname.like(appname+'%'),
				DeployLogDB.user.like(user+'%'),
				DeployLogDB.submit_time > start_time,
				DeployLogDB.submit_time < end_time
				).order_by(desc('submit_time')).order_by(desc('submit_time'))
		else:
			deployloglist = DeployLogDB.query.filter(DeployLogDB.appname.like(appname+'%'),
				DeployLogDB.user.like(user+'%')
				).order_by(desc('submit_time')).order_by(desc('submit_time'))

		for deploylog in deployloglist:
			deploylogdict[deploylog.id] = deploylog.to_json()
		return jsonify(result=deploylogdict)
