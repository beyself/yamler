# encoding:utf8

from flask import Blueprint,request,render_template,session,flash,redirect,url_for,jsonify
from yamler.models.users import User,RegistrationForm,LoginForm
from yamler.database import db_session
from yamler.utils import request_wants_json, required_login

mod = Blueprint('user',__name__,url_prefix='/user')

@mod.route('/')
def index():
    print request.form
    return 'ok'

@mod.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data,form.password.data)
        result = User.query.filter_by(username = user.username).filter_by(password = user.password).first()
        if result:
            session['user_id']=result.id
            #session['group_id'] = result.group_id
            #session['company_id'] = result.company_id
            return redirect(url_for('home.myfeed'))
    return render_template('user/login.html',form=form)

@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method=='POST' and form.validate():
        user=User(form.username.data, 
                    form.password.data, 
                    is_active=1,
                    realname = request.form['realname'] if request.form.has_key('realname')   else '',
                   )
        result = User.query.filter_by(username=user.username).first()
        if result:
            return redirect(url_for('user.register'))
        db_session.add(user)
        db_session.commit()
        session['user_id']=user.id 
        flash('Thanks for registering')
        return redirect(url_for('company.create'))
    return render_template('user/register.html', form=form)

@mod.route('/active', methods=['GET', 'POST'])
def active():
    return render_template('user/active.html')
