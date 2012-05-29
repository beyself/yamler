# encoding:utf8
import datetime
from flask import Blueprint,request,render_template,session, g, jsonify
from yamler.models.users import User,RegistrationForm,LoginForm
from yamler.database import db_session, conn
from yamler import app
from yamler.utils import required_login
from yamler.models.companies import companies
from yamler.models.groups import groups 
from yamler.models.tasks import tasks, task_comments
from sqlalchemy.sql import select, text

mod = Blueprint('home', __name__, url_prefix='/home')

@mod.route('/')
@required_login
def index():
    return 'ok'

@mod.route('/myfeed', methods=['GET', 'POST'])
def myfeed():
    group_rows = conn.execute(select([groups, groups.c.company_id==18])).fetchall()
    return render_template('home/myfeed.html', group_rows=group_rows, pagename='myfeed', args=request.args)

@mod.route('/mytask', methods=['GET', 'POST'])
def mytask():
    s = text("SELECT id,user_id,to_user_id,title,created_at,end_time,status FROM tasks WHERE user_id = :user_id") 
    task_rows = conn.execute(s, user_id=g.user.id).fetchall()
    return render_template('home/mytask.html', task_rows=task_rows, pagename='mytask') 

@mod.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST' and request.form['title']:
        conn.execute(tasks.insert().values({tasks.c.title: request.form['title'], 
                                            tasks.c.user_id: g.user.id,
                                            tasks.c.created_at: datetime.datetime.now(), 
                                            tasks.c.to_user_id: request.form['to_user_id'].lstrip(',')
                                           })) 
        return jsonify(title=request.form['title'], ismine=True, realname=g.user.realname, share_users=request.form['share_users'])

@mod.route('/getMyFeed')
def getMyFeed():
    t = int(request.args.get('t',0))
    if t == 1:
        rows = conn.execute(text("SELECT id,user_id,to_user_id,title,created_at,end_time,status FROM tasks WHERE user_id=:user_id ORDER BY created_at DESC"),user_id=g.user.id).fetchall();
        print rows
    elif t == 2:
        rows = conn.execute(text("SELECT id,user_id,to_user_id,title,created_at,end_time,status FROM tasks WHERE to_user_id IN (:to_user_id) ORDER BY created_at DESC"),to_user_id=g.user.id).fetchall();
    else:
        s = text("SELECT id,user_id,to_user_id,title,created_at,end_time,status FROM tasks WHERE user_id = :user_id UNION ALL SELECT id,user_id,to_user_id,title,created_at,end_time,status FROM tasks WHERE to_user_id IN (:to_user_id) ORDER BY created_at DESC") 
        rows = conn.execute(s, user_id=g.user.id, to_user_id=g.user.id).fetchall()
    user_sql = text("SELECT GROUP_CONCAT( realname ) AS share_users FROM `users` WHERE id IN ( :id )")
    data = []
    #user_sql = "SELECT GROUP_CONCAT( realname ) AS share_users FROM `users` WHERE id IN :id "
    for row in rows:
        new_row = {}
        new_row['id'] = row['id']
        new_row['user_id'] = row['user_id'] 
        new_row['created_at'] = row['created_at'].strftime('%Y-%m-%d %T') if row['created_at'] else ''
        new_row['title'] = row['title'] 
        new_row['status'] = row['status'] 
        if row['to_user_id']:
            sql = "SELECT GROUP_CONCAT( realname ) AS share_users FROM `users` WHERE id IN ("
            to_ids = ''
            for s in row['to_user_id'].split(','):
                if s:
                    to_ids += s.strip()+','
            to_ids = to_ids.rstrip(',')
            if to_ids != '0':
                sql += to_ids
                sql += ")" 
                result = conn.execute(text(sql)).first()
                new_row['share_users'] = result['share_users'] 
        if row['user_id'] == g.user.id:
            new_row['realname'] = g.user.realname
            new_row['ismine'] = True 
        else:
            result = conn.execute(text("SELECT realname FROM users WHERE id=:id"),id=row['user_id']).first()
            new_row['realname'] = result['realname'] 
            new_row['other'] = True 
        data.append(new_row)
    return jsonify(data=data)
