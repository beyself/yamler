#!/usr/bin/env python
# encoding: utf-8
from flask import app
from flup.server.fcgi import WSGIServer
WSGIServer(app,bindAddress='/tmp/yamler.sock').run()
