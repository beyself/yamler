# encoding:utf8

from flask import Blueprint,request,render_template,session,flash,redirect,url_for,jsonify
from yamler.database import db_session
from yamler.models.companies import Company,CompanyForm 

mod = Blueprint('company',__name__,url_prefix='/company')

@mod.route('/create',methods=['GET','POST'])
def create():
    form = CompanyForm(request.form)
    if request.method == 'POST' and form.validate():
        company = Company(user_id = session['user_id'],name=form.name.data,scale=form.scale.data,contact_name=form.contact_name.data,telephone=form.telephone.data,website=form.website.data,address=form.address.data,postcode=form.postcode.data)
        db_session.add(company)
        db_session.commit()
    return render_template('company/create.html',form=form)
