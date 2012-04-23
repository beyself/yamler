#encoding:utf8
from sqlalchemy import Column, Integer, String, DateTime
from yamler.database import Model  
import datetime

class UserRelation(Model):
    __tablename__ = 'user_relations'
    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer)
    to_user_id = Column(Integer)
    status = Column(Integer, default='0')
    created_at = Column(DateTime,default=datetime.datetime.now())
    updated_at = Column(DateTime,default=datetime.datetime.now())

    def __init__(self, from_user_id=None, to_user_id=None, status='0'):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.status = status

    def __repr__(self):
        return '<UserRelation %d %d %d>' % (self.from_user_id, self.to_user_id, self.status)
    
    def to_json(self):
        return dict(id = self.id,
                    from_user_id = self.from_user_id,
                    to_user_id = self.to_user_id,
                    status = self.status
                )
