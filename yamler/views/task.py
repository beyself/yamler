# encoding:utf8
from flask import Blueprint,request,render_template,session, g,jsonify
from yamler.database import conn 
from sqlalchemy.sql import select, text
from yamler.models.tasks import tasks
from yamler.models.users import users 
import json

mod = Blueprint('task', __name__, url_prefix='/task')

@mod.route('/create')
def create():
    pass

@mod.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    
    row = conn.execute(text("SELECT id,user_id,to_user_id,title,created_at,end_time,status FROM tasks WHERE id=:id"), id=id).first()
    row = dict(row)
    row['share_users'] = []
    if row and row.has_key('to_user_id') and row['to_user_id']:
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
                row['share_users'] = result['share_users'].split(',')
    company_users = conn.execute(select([users.c.id, users.c.realname],users.c.company_id==g.company.id)).fetchall()
    data_users = [] 
    for company_row in company_users:
        data_users.append({'value': company_row['realname'], 'id': company_row['id']})
    return render_template('task/update.html', row=row, data_users=json.dumps(data_users), share_users_default=json.dumps(row['share_users'])) 
