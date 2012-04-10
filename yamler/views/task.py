# encoding:utf8
from flask import Blueprint,request,render_template,session
from yamler.database import db_session

mod = Blueprint('task', __name__, url_prefix='/task')

@mod.route('/create')
def create():
    pass
