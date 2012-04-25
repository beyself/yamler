# encoding:utf-8
from flask import Blueprint, request, session, jsonify
from yamler.database import db_session
from yamler.models.users import User
from yamler.models.tasks import Task
from yamler.models.user_relations import UserRelation 
from sqlalchemy.sql import between
from sqlalchemy import or_

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
                    to_user_id = request.form['to_user_id'] if request.form.has_key('to_user_id') else 0,
                    note = request.form['note'] if request.form.has_key('note') else '', 
                    priority = request.form['priority'] if request.form.has_key('priority') else 1, 
                    end_time = request.form['end_time'] if request.form.has_key('end_time') else '',
                    ) 
        db_session.add(task)
        db_session.commit()
        return jsonify(error=0, code='success', message='添加成功')
    return jsonify(error=1, code='failed', message='输入数据不合法')

@mod.route('/task/get',methods=['POST'])
def task_get():
    if request.form['user_id'] and request.form['status']:
        #rows = db_session.query(Task).filter(between(Task.created_at, request.form['start_time'], request.form['end_time'])).filter_by(user_id = request.form['user_id']).all()
        rows = db_session.query(Task).filter_by(user_id = request.form['user_id']).filter_by(status = request.form['status'])
        data = [row.to_json() for row in rows]
        return jsonify(error = 0, data = data)
    return jsonify(error = 1, data = {}) 

@mod.route('/task/update', methods=['POST'])
def task_update():
    if request.method == 'POST' and request.form['id'] and request.form['user_id']:
        task = db_session.query(Task).get(request.form['id']) 
        if task and task.user_id == int(request.form['user_id']) :
            if request.form.has_key('status') : 
                task.status = request.form['status']
            if request.form.has_key('title'):
                task.title = request.form['title']
            if request.form.has_key('note'):
                task.note = request.form['note']
            if request.form.has_key('priority'):
                task.priority = request.form['priority']
            if request.form.has_key('end_time'):
                task.end_time = request.form['end_time']
            if request.form.has_key('to_user_id'):
                task.to_user_id = request.form['to_user_id']
            db_session.commit()
            return jsonify(error=0, code='success', message='修改成功', id=task.id)
    
    return jsonify(error=1, code='failed', message='修改失败')

@mod.route('/task/delete', methods=['POST'])
def task_delete():
    if request.method == 'POST' and request.form['id'] and request.form['user_id']:
        task = db_session.query(Task).get(request.form['id']) 
        if task and task.user_id == int(request.form['user_id']) :
            db_session.delete(task)
            db_session.commit()
            return jsonify(error=0, code='success', message='删除成功', id=task.id)

    return jsonify(error=1, code='failed', message='删除失败')

@mod.route('/rel/create', methods=['POST'])
def rel_create():
    if request.method == "POST" and request.form['user_id'] and request.form['username']:
        user = db_session.query(User).filter_by(username=request.form['username']).first() 
        if user is None:
            return jsonify(error=1, code='empty', message='用户名不存在')
        user_relations = db_session.query(UserRelation).filter_by(from_user_id=request.form['user_id']).filter_by(to_user_id=user.id).first()
        if user_relations is None:
            from_user = db_session.query(User).get(request.form['user_id'])
            rel = UserRelation(from_user_id=request.form['user_id'], to_user_id=user.id, status=0, from_user_name=from_user.username, to_user_name=request.form['username'])
            db_session.add(rel)
            db_session.commit()
            return jsonify(error=0, code='success', from_user_id=rel.from_user_id, to_user_id=rel.to_user_id, status=rel.status)

        return jsonify(error=0, code='success', from_user_id=request.form['user_id'], to_user_id=user_relations.to_user_id, status=user_relations.status)
    return jsonify(error=1, code='failed', message='参数传递不正确')

@mod.route('/rel/update', methods=['POST'])
def rel_update():
    if request.method == 'POST' and request.form['id'] and request.form['user_id']:
        rel = db_session.query(UserRelation).get(request.form['id'])
        if rel and rel.to_user_id == int(request.form['user_id']):
            if request.form.has_key('status'):
                rel.status = request.form['status']
            db_session.commit()
            return jsonify(error=0, code='success', from_user_id=rel.from_user_id, to_user_id=rel.to_user_id, status=rel.status)
    
    return jsonify(error=1, code='failed', message='参数传递不正确')

@mod.route('/rel/get', methods=['POST'])
def rel_get():
    if request.method == 'POST':
        if request.form.has_key('to_user_id') and request.form.has_key('status'):
            rows = db_session.query(UserRelation).filter_by(to_user_id=request.form['to_user_id']).filter_by(status=request.form['status']).all() 
        elif request.form.has_key('from_user_id') and request.form.has_key('status'):
            rows = db_session.query(UserRelation).filter_by(from_user_id=request.form['from_user_id']).filter_by(status=request.form['status']).all() 
        elif request.form.has_key('user_id') and request.form.has_key('status'):
            rows = db_session.query(UserRelation).filter(or_(UserRelation.from_user_id==request.form['user_id'],UserRelation.to_user_id==request.form['user_id'])).filter_by(status=request.form['status']).all()
        data = [row.to_json() for row in rows]
        return jsonify(error=0, data=data)
