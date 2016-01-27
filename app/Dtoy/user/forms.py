#-*- coding: UTF-8 -*-   

from flask.ext.wtf import Form
from wtforms import IntegerField,SelectField,TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User


class UseraddForm(Form):
  nickname = TextField(u"昵称",  [validators.Required("Please enter your first name."),validators.Length(max=24)])
  username = TextField(u"用户名",  [validators.Required("Please enter your last name."),validators.Length(max=24)])
  identity = SelectField(u'角色', choices=[(u'管理员',u'管理员'), (u'用户',u'用户'), (u'游客',u'游客')])
  email = TextField(u"邮件",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField(u'密码', [validators.Required("Please enter a password."),validators.Length(min=6,max=100)])
  submit = SubmitField(u"创建用户")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class LoginForm(Form):
  email = TextField(u"邮箱帐号",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField(u'密码', [validators.Required("Please enter a password.")])
  submit = SubmitField(u"登录")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False

class HaproxySearchForm(Form):
  platname = SelectField(u'选择平台', choices=[('hf.21tb.com','hf.21tb.com'), ('cloud.21tb.com','cloud.21tb.com')])
  pxname = TextField(u"应用名称",  [validators.Length(min=4, max=25)])
  submit = SubmitField(u"GO")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return True
    else:
      return True

class HaproxyConfModuleForm(Form):
  modulename = TextField('modulename')
  submit = SubmitField(u"预览")

  def __init__(self,*args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return True
    else:
      return True


class UploadMiddleConf(Form):
  name = TextField(u"版本名称",  [validators.Required(u"请输入配置名称，不可重复"),validators.Length(max=60)])
  middletype = TextField(u"中间件类型",  [validators.Required(u"请输入中间件类型"),validators.Length(max=60)])
  module = TextField(u"模块",  [validators.Required(u"具体类型模块"),validators.Length(max=60)])
  context = TextField(u"内容",  [validators.Required(u"配置内容")])
  submit = SubmitField(u"上传")

  def __init__(self,*args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True


class CommonSearchForm(Form):
  infotype = TextField(u"类型",  [validators.Required(u"请输入查询类型")])
  host = TextField(u"主机",  [validators.Required(u"请输入链接地址")])
  port = IntegerField(u'端口', [validators.required()])
  pxname = TextField(u"查询",  [validators.required()])
  extra = TextField(u'附注')
  submit = SubmitField(u"GO")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return True
    else:
      return True
