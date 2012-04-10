#encoding:utf8

import re
from flask import g, url_for, flash, abort, request, redirect, Markup, session

def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

def required_login():
    return session['user_id']
