from flask import Flask,session,g,render_template
app = Flask(__name__)
app.config.from_object('config')
from yamler.database import db_session

from yamler.views import home
app.register_blueprint(home.mod)

