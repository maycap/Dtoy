#-*- coding: UTF-8 -*-   

from flask.ext.wtf import Form
from wtforms import IntegerField,SelectField,TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db


class AppInfoForm(Form):
  appname = TextField(u"应用名称")
  apptype = SelectField(u"应用类型",  choices=[('app','app'),('paas','paas'),('framework','framework')])
  branch = TextField(u"分支")
  typeinfo = SelectField(u'git类型', choices=[(u'ssh',u'ssh'), (u'https',u'https'), (u'http',u'http')])
  remarks = TextField(u"备注")
  submit = SubmitField(u"添加")


  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return True
    else:
      return True

class DeployForm(Form):
  appname = SelectField(u"应用名称",  [validators.Required(u"请输入项目名称")])
  branch = TextField(u"分支",  [validators.Required(u"请输入git分支")])
  submit = SubmitField(u"GO")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return True
    else:
      return True