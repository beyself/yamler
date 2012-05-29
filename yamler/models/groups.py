#encoding:utf8

from sqlalchemy import Column,Integer,String,DateTime, Table
from yamler.database import Model, metadata
import datetime
from wtforms import Form, TextField, validators

class Group(Model): 
    __tablename__ = 'groups'
    id = Column(Integer,primary_key=True)
    company_id = Column(Integer)
    title = Column(String(45)) 
    created_at = Column(DateTime,default=datetime.datetime.now())
    updated_at = Column(DateTime,default=datetime.datetime.now())

    def __init__(self, title=None, company_id=None):
        self.company_id = company_id
        self.title = title

    def __repr__(self):
        return "<Group ('%s')>" % (self.title)

groups = Table('groups', metadata, autoload=True)

class GroupForm(Form):
    title = TextField('名称',validators=[validators.Length(max=100)])
