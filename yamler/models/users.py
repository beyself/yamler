#encoding:utf8
import datetime,hashlib
from sqlalchemy import Column, Integer, String, DateTime
from yamler.database import Model  
from wtforms import Form, BooleanField, TextField, PasswordField, validators

class User(Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(32))
    realname = Column(String(45))
    is_active = Column(Integer)
    created_at = Column(DateTime,default=datetime.datetime.now())
    updated_at = Column(DateTime,default=datetime.datetime.now())

    def __init__(self, username=None, password=None,is_active=None, realname=None):
        self.username = username
        self.is_active = is_active
        self.password = hashlib.md5(password).hexdigest() 
        self.realname = realname

    def __repr__(self):
        return '<User %r>' % (self.username)

    def to_json(self):
        result = dict(id=self.id,
                      username=self.username,
                      password=self.password,
                      realname=self.realname,
                      is_active=self.is_active,
                      created_at=self.created_at,
                     )
        return result

class RegistrationForm(Form):
    username = TextField('帐户', [validators.Length(min=4, max=25)])
    password = PasswordField('密码', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('确认密码')
    accept_tos = BooleanField('我同意注册协议', [validators.Required()])

class LoginForm(Form):
    username = TextField('帐户', validators=[validators.required()])
    password = TextField('密码', validators=[validators.required()])
