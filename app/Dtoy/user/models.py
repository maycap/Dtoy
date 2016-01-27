#-*- coding: UTF-8 -*-   

from Dtoy import db
from werkzeug import generate_password_hash, check_password_hash


class User(db.Model):
  __tablename__ = 'users'
  __table_args__ = {'sqlite_autoincrement': True}
  uid = db.Column(db.Integer, primary_key = True)
  nickname = db.Column(db.String(100))
  username = db.Column(db.String(100))
  identity = db.Column(db.String(40))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
  
  def __init__(self, nickname, username,identity, email, password):
    self.nickname = nickname.title()
    self.username = username.title()
    self.identity = identity.title()
    self.email = email.lower()
    self.set_password(password)

    
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)


  def is_authenticated(self):
      return True

  def is_active(self):
      return True

  def is_anonymous(self):
      return False

  def get_id(self):
      return unicode(self.uid)

  def __repr__(self):
      # return '<User %r>' % (self.email)
      return '%s' % (self.email)



