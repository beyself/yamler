# encoding:utf8
from flask import Blueprint,request,render_template,session
from yamler.models.groups import Group, GroupForm
from yamler.database import db_session

mod = Blueprint('group', __name__, url_prefix='/group')

@mod.route('/create')
def create():
    pass
