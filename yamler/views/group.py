# encoding:utf8
from flask import Blueprint,request,render_template,session, g
from yamler.models.groups import Group, GroupForm
from yamler.database import db_session

mod = Blueprint('group', __name__, url_prefix='/group')

@mod.route('/')
def index():
    return 'ok'

@mod.route('/create', methods=['GET', 'POST'])
def create():
    form=GroupForm(request.form)
    if request.method=='POST' and form.validate():
        group = Group(title=form.title.data,
                      company_id=g.company.id,
                     )
        db_session.add(group)
        db_session.commit()
        #return redirect(url_for('group'))
    return render_template('group/create.html', form=form)
