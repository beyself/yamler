#encoding:utf8

from sqlalchemy import Column,Integer,String,DateTime
from yamler.database import Model
import datetime
from wtforms import Form, TextField, validators

class Group(Model): 
    __tablename__ = 'groups'
    id = Column(Integer,primary_key=True)
    company_id = Column(Integer)
    title = Column(String(45)) 
    created_at = Column(DateTime,default=datetime.datetime.now())
    updated_at = Column(DateTime,default=datetime.datetime.now())

    def __init__(self,title,company_id):
        self.company_id = company_id
        self.title = title

    def __repr__(self):
        return "<Group ('%s')>" % (self.title)

class GroupForm(Form):
    title = TextField('名称',validators=[validators.Required])
