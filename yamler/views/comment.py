#-*- encoding:utf-8 -*-
import datetime
from flask import Blueprint,request,render_template,session, g, jsonify
from yamler.models.tasks import tasks, task_comments
from sqlalchemy.sql import select, text
from yamler.database import conn

mod = Blueprint('comment', __name__, url_prefix='/comment')

@mod.route('/get/<int:task_id>')
def get(task_id):
    comment_rows = conn.execute(text("SELECT id, task_id, user_id, content, created_at FROM task_comments WHERE task_id=:task_id"), task_id=task_id).fetchall() 
    data = []
    for row in comment_rows:
        new_row = {'id': row['id'], 'user_id': row['user_id'], 'content': row['content']} 
        new_row['created_at'] = row['created_at'].strftime('%Y-%m-%d %T')
        if row['user_id'] != g.user.id:
            result = conn.execute(text("SELECT id, realname from users WHERE id=:user_id LIMIT 1"), user_id=row['user_id']).first()
            new_row['realname'] = result['realname']
        else:
            new_row['realname'] = g.user.realname

        data.append(new_row)
    return jsonify(data=data, task_id=task_id) 

@mod.route('/create/<int:task_id>', methods=['POST'])
def create(task_id):
    if request.form['comment_content'] and g.user.id:
        created_at = datetime.datetime.now()
        conn.execute(task_comments.insert().values({task_comments.c.user_id: g.user.id, 
                                                    task_comments.c.task_id: task_id, 
                                                    task_comments.c.content: request.form['comment_content'], 
                                                    task_comments.c.created_at: created_at,
                                                   }))
        return jsonify(content=request.form['comment_content'], task_id=task_id, realname=g.user.realname, created_at=created_at.strftime('%Y-%m-%d %T'))
