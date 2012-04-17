#encoding:utf8
import datetime,time
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from yamler.database import Model 
from werkzeug import http_date

class Task(Model):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Integer, default = 0)
    note = Column(String(200),default='')
    priority = Column(Integer, default=1)
    end_time = Column(DateTime,default = '') 
    created_at = Column(DateTime, default=datetime.datetime.now()) 
    updated_at = Column(DateTime,default=datetime.datetime.now()) 

    def __init__(self, title, user_id, note=None, priority=None, end_time=None):
        self.title = title
        self.note = note
        self.user_id = user_id
        self.priority = priority
        self.end_time = end_time


    def __repr__(self):
        return '<Task %r>' % (self.title)

    def to_json(self):
        result = dict(title = self.title, note = self.note, user_id = self.user_id, priority = self.priority, status = self.status, created_at = self.created_at.strftime('%Y-%m-%d %T')) 
        if self.end_time: 
            result['end_time'] = self.end_time.strftime('%Y-%m-%d %T')
        else:
            result['end_time'] = '' 

        return result



