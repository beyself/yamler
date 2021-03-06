#encoding:utf8
import datetime,time
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from yamler.database import Model, metadata 
from werkzeug import http_date
from wtforms import Form, TextField, validators

class Task(Model):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    user_id = Column(Integer, ForeignKey('users.id'))
    to_user_id = Column(String(45), default=0)
    status = Column(Integer, default = 0)
    note = Column(String(200),default='')
    description = Column(String(500),default='')
    priority = Column(Integer, default=1)
    end_time = Column(DateTime,default = '') 
    created_at = Column(DateTime, default=datetime.datetime.now()) 
    updated_at = Column(DateTime,default=datetime.datetime.now()) 

    def __init__(self, title, user_id, note=None, priority=None, end_time=None, to_user_id=None):
        self.title = title
        self.note = note
        self.user_id = user_id
        self.to_user_id = to_user_id
        self.priority = priority
        self.end_time = end_time


    def __repr__(self):
        return '<Task %r>' % (self.title)

    def to_json(self):
        result = dict(id = self.id, title = self.title, description=self.description, note = self.note, user_id = self.user_id, to_user_id=self.to_user_id, priority = self.priority, status = self.status, created_at = self.created_at.strftime('%Y-%m-%d %T')) 
        if self.end_time: 
            result['end_time'] = self.end_time.strftime('%m-%d %l:%M %p')
        else:
            result['end_time'] = '' 

        return result

class TaskComment(Model):
    __tablename__ = 'task_comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    task_id = Column(Integer)
    content = Column(String(200))  
    created_at = Column(DateTime, default=datetime.datetime.now()) 
    updated_at = Column(DateTime,default=datetime.datetime.now()) 

    def __init__(self, user_id, task_id, content):
        self.user_id = user_id
        self.task_id = task_id
        self.content = content
        

tasks = Table('tasks', metadata, autoload=True)
task_comments = Table('task_comments', metadata, autoload=True)

class TaskForm(Form):
    title = TextField('标题', [validators.required()])

