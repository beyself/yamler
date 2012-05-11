#encoding:utf8
import re
from flask import g, url_for, flash, abort, request, redirect, Markup, session

def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

def required_login(f):
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'需要登录才能访问')
            return redirect(url_for('user.login', next=request.path))
        if g.user.is_active == 0:
            flash(u'账户还未激活，请等待......')
            return redirect(url_for('user.active'))
        return f(*args, **kwargs)
    return decorated_function


def required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.is_admin:
            abort(401)
            return f(*args, **kwargs)
    return requires_login(decorated_function)


