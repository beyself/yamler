#encoding:utf8

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from yamler.database import Model  

class Task(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    note = Column(String(200))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(datetime,default=datetime.datetime.now()) 
    updated_at = Column(datetime,default=datetime.datetime.now()) 

    def __init__(sefl):
        pass
