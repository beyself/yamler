#encoding:utf8

from sqlalchemy import Column, Integer, String
from yamler.database import Model  
from flaskext.wtf import Form, BooleanField, TextField, PasswordField, validators

class User(Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(32))
    #created_at = Column(DateTime)
    #updated_at = Column(DateTime)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password 

    def __repr__(self):
        return '<User %r>' % (self.name)
 
class RegistrationForm(Form):
    username = TextField('Username', [validators.Required(),validators.Length(min=4,max=20)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [validators.Required()])
    accept_tos = BooleanField('I accept the TOS', [validators.Required])

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = TextField('Password', [validators.Required()])
