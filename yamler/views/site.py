#-*- encoding:utf-8 -*-
from flask import Blueprint, request, render_template

mod = Blueprint('site',__name__)

@mod.route('/')
def index():
    return render_template('site/index.html')
