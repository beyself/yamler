# encoding:utf-8
from flask import Blueprint, request, session, jsonify
from yamler.database import db_session
from yamler.models.users import User

mod = Blueprint('mobile',__name__,url_prefix='/mobile')

@mod.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username and password:
        user = User(username,password)
        result = User.query.filter_by(username=user.username, password=user.password).first()
        if result:
            session['user_id'] = result.id
            return jsonify(error=0, code='success', message='登录成功')
        else:
            return jsonify(error=1, code='username_or_password_error',message='用户名或密码错误')
    else:
        return jsonify(error=1, code='no_username_or_password', message='没有输入用户名或密码')

@mod.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username and password:
        user = User(username,password,is_active=1)
        result = User.query.filter_by(username = user.username).first() 
        if result:
            return jsonify(error=1, code='username_exists', message='用户名已经存在')
        else:
            db_session.add(user)
            db_session.commit()
            return jsonify(error=0, code='success', message='成功注册')

    return jsonify(error=1, code = 'no_username_or_password', message='没有输入用户名或密码')
