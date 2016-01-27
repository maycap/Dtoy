# -*- coding: utf-8 -*-

from Dtoy import app,socketio
from DeployView import Deploy_View,AppInfoAdd_View,AppInfoManager_View,Branch_View,DeployLog_View

# from flask_login import current_user
# from flask_socketio import SocketIO, emit





deploy_view = Deploy_View.as_view('deploy/deploy')
appinfoadd_view = AppInfoAdd_View.as_view('deploy/appinfoadd')
appinfomanager_view = AppInfoManager_View.as_view('deploy/appinfomanager')
branch_view = Branch_View.as_view('deploy/branch')
deploylog_view = DeployLog_View.as_view('deploy/deploylog')

# app.add_url_rule('/salt/', defaults={'cmd': None},view_func=salt_view, methods=['GET',])
app.add_url_rule('/deploy/deploy', view_func=deploy_view, methods=['GET','POST'])
app.add_url_rule('/deploy/appinfoadd', view_func=appinfoadd_view,methods=['GET','POST'])
app.add_url_rule('/deploy/appinfomanager', view_func=appinfomanager_view,methods=['GET','POST'])
app.add_url_rule('/deploy/branch',view_func=branch_view,methods=['POST'])
app.add_url_rule('/deploy/deploylog',view_func=deploylog_view,methods=['GET','POST'])



# @socketio.on('my event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     if current_user.is_authenticated:
# 		emit('my response',
# 		     {'data': message['data'], 'count': session['receive_count']})

