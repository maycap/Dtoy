# -*- coding: utf-8 -*-

from Dtoy import app
from UserView import User_View,Login_View,Home_View,Logout_View,UserAdd_View,UserManage_View,UserProfile_View
from flask import g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.login import LoginManager
from models import User


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


home_view = Home_View.as_view('home')

app.add_url_rule('/',view_func=home_view,methods=['GET',])
app.add_url_rule('/home',view_func=home_view,methods=['GET',])

user_view = User_View.as_view('user')
# user_required_view = login_required(user_view)

app.add_url_rule('/user/', defaults={'username': None},view_func=user_view, methods=['GET',])
app.add_url_rule('/user/', view_func=user_view, methods=['POST',])
# app.add_url_rule('/user/<string:username>', view_func=user_view,methods=['GET'])


login_view = Login_View.as_view('login')
app.add_url_rule('/login',view_func=login_view,methods=['GET','POST'])

logout_view = Logout_View.as_view('logout')
app.add_url_rule('/logout',view_func=logout_view,methods=['GET','POST'])

useradd_view = UserAdd_View.as_view('user/add')
app.add_url_rule('/user/add',view_func=useradd_view,methods=['GET','POST'])

usermange_view = UserManage_View.as_view('user/manage')
app.add_url_rule('/user/manage',view_func=usermange_view,methods=['GET','POST'])

userprofile_view = UserProfile_View.as_view('user/profile')
app.add_url_rule('/user/profile',view_func=userprofile_view,methods=['GET','POST'])




