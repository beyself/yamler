# encoding:utf8

from flask import Blueprint,request,render_template,session,flash,redirect,url_for,jsonify
from yamler.models.users import User,RegistrationForm,LoginForm
from yamler.database import db_session
from yamler.utils import request_wants_json

mod = Blueprint('user',__name__,url_prefix='/user')

@mod.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data,form.password.data)
        result = User.query.filter_by(username = user.username).filter_by(password = user.password).first()
        if result:
            session['user_id'] = result.id
            #session['group_id'] = result.group_id
            #session['company_id'] = result.company_id
            if request_wants_json():
                return jsonify(error = 0,message = 'login success')
        else:
            if request_wants_json():
                return jsonify(error = 1,message = 'login failed')
    return render_template('user/login.html',form=form)

@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data, is_active=1)
        db_session.add(user)
        db_session.commit()
        flash('Thanks for registering')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)
