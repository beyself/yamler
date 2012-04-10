#encoding:utf8
import datetime
from sqlalchemy import Column, Integer, String
from yamler.database import Model  

class Keyword(Model):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(String(45), unique=True)
    created_at = Column(datetime,default=datetime.datetime.now()) 
    updated_at = Column(datetime,default=datetime.datetime.now()) 

    def __init__(self,keyword):
        self.keyword = keyword

    def __repr__(self):
        return "<Keyword('%s'>" % (self.keyword)
    
class KeywordCount(Model):
    __tablename__ = 'keyword_counts'
    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer)
    count = Column(Integer)
    created_at = Column(datetime,default=datetime.datetime.now()) 
    updated_at = Column(datetime,default=datetime.datetime.now()) 

    def __init__(self,keyword_id,count):
        self.keyword_id = keyword_id
        self.count = count

    def __repr__(self):
        return "<KeywordCount('%d','%d'>" % (self.keyword_id,self.count)
