#!/usr/bin/python3
'''
'''

from flask import Flask
import wtforms as wtf

app = Flask(__name__)

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
