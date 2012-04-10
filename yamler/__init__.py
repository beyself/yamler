#encoding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask,session,g,render_template

app = Flask(__name__)
app.config.from_object('config')
from yamler.database import db_session

from yamler.views import home
from yamler.views import user
from yamler.views import company
from yamler.views import group
from yamler.views import task
from yamler.views import mobile 

app.register_blueprint(home.mod)
app.register_blueprint(user.mod)
app.register_blueprint(company.mod)
app.register_blueprint(group.mod)
app.register_blueprint(task.mod)
app.register_blueprint(mobile.mod)
