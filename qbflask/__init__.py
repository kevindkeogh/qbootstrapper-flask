#!/usr/bin/python3
'''
'''

from flask import Flask
import wtforms as wtf
from flask_wtf import csrf

app = Flask(__name__)
csrf.CSRFProtect().init_app(app)  # enable CSRF protection

import qbflask.views
import qbflask.forms


app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='secret',
    USERNAME='admin',
    PASSWORD='admin'
))

if __name__ == '__main__':
    app.run()
