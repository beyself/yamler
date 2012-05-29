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
from yamler.views import site 
from yamler.views import comment 

app.register_blueprint(home.mod)
app.register_blueprint(user.mod)
app.register_blueprint(company.mod)
app.register_blueprint(group.mod)
app.register_blueprint(task.mod)
app.register_blueprint(mobile.mod)
app.register_blueprint(site.mod)
app.register_blueprint(comment.mod)

from yamler.models.users import User
from yamler.models.companies import Company 

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.before_request
def load_current_user():
    g.user = User.query.filter_by(id=session['user_id']).first() if 'user_id' in session else None
    g.company = Company.query.filter_by(id=g.user.company_id).first() if g.user else None

@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


