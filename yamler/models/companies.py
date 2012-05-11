#encoding:utf8

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from yamler.database import Model, metadata
import datetime
from wtforms import Form, TextField, SelectField, validators

class Company(Model):
    __tablename__ = 'companies'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer)
    name = Column(String(100))
    scale = Column(Integer)
    contact_name = Column(String(45))
    telephone = Column(String(45))
    address = Column(String(150))
    postcode = Column(String(45))
    website = Column(String(100))
    created_at = Column(DateTime,default=datetime.datetime.now()) 
    updated_at = Column(DateTime,default=datetime.datetime.now()) 

    def __init__(self,user_id,name=None, scale=None, contact_name=None, telephone=None, address=None, postcode=None, website=None):
        self.user_id = user_id
        self.name = name
        self.scale = scale
        self.contact_name = contact_name
        self.telephone = telephone
        self.address = address
        self.postcode = postcode
        self.website = website

    def __repr__(self):
        return "<Company ('%s','%s','%s','%s','%s','%s','%s')>" % (self.name, self,scale, self.contact_name, self.telephone, self.address, self.postcode, self.website)

companies = Table('companies', metadata, autoload=True)
 

class CompanyForm(Form):
    SCALE_VALUES = [
        ('1','5人以下'),
        ('2','5-10人'),
        ('3','10-20人'),
        ('4','20-30人'),
        ('5','30-50人'),
        ('6','50-70人'),
        ('7','70-100人'),
        ('8','100-200人'),
        ('9','200-500人'),
        ('10','500人以上'),
    ]
    contact_name = TextField('联系人',validators=[validators.Length(max=100)])
    name = TextField('企业名称',validators=[validators.Length(max=100)])
    scale = SelectField('公司规模',choices=SCALE_VALUES)
    telephone = TextField('联系电话',validators=[validators.Length(max=45)])
    address = TextField('地址',validators=[validators.Length(max=150)])
    postcode = TextField('邮编',validators=[validators.Length(max=45)])
    website = TextField('网址',validators=[validators.Length(max=100)])
