# encoding:utf8
from flask import Blueprint,request,render_template,session
from yamler.models.users import User,RegistrationForm,LoginForm
from yamler.database import db_session
from flaskext.login import *
from yamler import app

mod = Blueprint('home', __name__)

@mod.route('/')
def index():
    u = User('xiudong','123456')
    db_session.add(u)
    db_session.commit()
    user = User.query.all()
    print user 
    return "Hello world"

@mod.route('/register',methods=['GET','POST'])
def register():
    form = form = RegistrationForm(request.form) 
    if request.method == 'POST' and form.validate():
        user = User(form.username.data,form.password.data)
        db_session.add(user)
    return render_template('home/register.html',form=form)

@mod.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(username='xiudong').first()
        if user.id:
            print user.id
            session['user_id'] = user.id
    return render_template('home/login.html',form=form)

@mod.route('/logout')
def logout():
    if 'uid' in session:
        del session['uid']

@mod.route('/test')
def test():
    user = User.query.filter(User.username == 'xiudong',User.password == '123456').first() 
    user = User.query.filter_by(username = 'xiudong').filter_by(password='123456').first() 
    print user.id
    return 'hello'
