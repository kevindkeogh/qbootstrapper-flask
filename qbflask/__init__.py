#!/usr/bin/python3
'''qbootstraper main application
'''

from flask import Flask
from flask_wtf import csrf

app = Flask(__name__)
csrf.CSRFProtect().init_app(app)  # enable CSRF protection

from qbflask.views import *


app.config.update(dict(
    DATABASE='qbflask.db',
    DEBUG=True,
    SECRET_KEY='secret',
    USERNAME='admin',
    PASSWORD='admin'
))

if __name__ == '__main__':
    app.run()
