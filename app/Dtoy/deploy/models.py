#-*- coding: UTF-8 -*-   

from Dtoy import db,app
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime


class AppInfoDB(db.Model):
  __tablename__ = 'appinfo'
  __table_args__ = {'sqlite_autoincrement': True}
  uid = db.Column(db.Integer, primary_key = True)
  appname = db.Column(db.String(100),unique=True)
  apptype = db.Column(db.String(20))
  giturl = db.Column(db.String(200))
  branch = db.Column(db.String(40))
  typeinfo = db.Column(db.String(40))
  submitter = db.Column(db.String(40))
  remarks = db.Column(db.String(200))
  
  def __init__(self, appname,apptype, giturl,branch, typeinfo, submitter,remarks):
    self.appname = appname
    self.apptype = apptype
    self.giturl = giturl
    self.branch = branch
    self.typeinfo = typeinfo
    self.submitter = submitter
    self.remarks = remarks

  def __repr__(self):
      # return '<User %r>' % (self.email)
      return '%s' % (self.appname)


class DeployLogDB(db.Model):
  __tablename__ = 'deploylog'
  __table_args__ = {'sqlite_autoincrement': True}
  id = db.Column(db.Integer, primary_key = True)
  appname = db.Column(db.String(50))
  user = db.Column(db.String(50))
  status = db.Column(db.String(100))
  submit_time = db.Column(db.DateTime, default=datetime.now())

  
  def __init__(self, appname,user, status,submit_time):
    self.appname = appname
    self.user = user
    self.status = status
    self.submit_time = submit_time

  def __repr__(self):
      # return '<User %r>' % (self.email)
      return '%s' % (self.appname)

  def to_json(self):
    return {
        'appname': self.appname,
        'user': self.user,
        'submit_time': self.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
    }


