# encoding:utf-8
from flask import Blueprint, request, session, jsonify
from yamler.database import db_session
from yamler.models.users import User
from yamler.models.tasks import Task
from sqlalchemy.sql import between

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
            return jsonify(error=0, code='success', message='登录成功', user_id = result.id)
        else:
            return jsonify(error=1, code='username_or_password_error',message='用户名或密码错误',)
    else:
        return jsonify(error=1, code='no_username_or_password', message='没有输入用户名或密码')

@mod.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username and password:
        user = User(username, password, is_active = 1)
        result = User.query.filter_by(username = user.username).first() 
        if result:
            return jsonify(error=1, code='username_exists', message='用户名已经存在')
        else:
            db_session.add(user)
            db_session.commit()
            return jsonify(error=0, code='success', message='成功注册', user_id = user.id)

    return jsonify(error=1, code = 'no_username_or_password', message='没有输入用户名或密码')

@mod.route('/task/create',methods=['POST'])
def task_create():
    if request.form['user_id'] and request.form['title']:
        task = Task(title = request.form['title'], 
                    user_id = request.form['user_id'], 
                    note = request.form['note'] if request.form.has_key('note') else '', 
                    priority = request.form['priority'] if request.form.has_key('priority') else 1, 
                    end_time = request.form['end_time'] if request.form.has_key('end_time') else '',
                    ) 
        db_session.add(task)
        db_session.commit()
        return jsonify(error=0, code='success', message='添加成功')
    return jsonify(error=1, code='failed', message='输入数据不合法')

@mod.route('/task/get',methods=['POST', 'GET'])
def task_get():
    if request.form['user_id'] and request.form['status']:
        #rows = db_session.query(Task).filter(between(Task.created_at, request.form['start_time'], request.form['end_time'])).filter_by(user_id = request.form['user_id']).all()
        rows = db_session.query(Task).filter_by(user_id = request.form['user_id']).filter_by(status = request.form['status'])
        data = [row.to_json() for row in rows]
        return jsonify(error = 0, data = data)
    return jsonify(error = 1, data = {}) 
