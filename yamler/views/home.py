# encoding:utf8
from flask import Blueprint,request,render_template
from yamler.models.users import User,RegistrationForm
from yamler.database import db_session

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
