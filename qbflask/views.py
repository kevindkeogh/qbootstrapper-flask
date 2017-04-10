#!/usr/bin/python3

from flask import request, render_template
from qbflask import app
from qbflask.forms import InstrumentList
import qbflask.bootstrapper as bstrap
import pprint

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InstrumentList()
    if request.method == 'POST':
        data = bstrap.parse_request(request)
        pprint.pprint(data)
    return render_template('index.html', form=form)

@app.route('/build_curve.html')
def build_curve():
    return "Hello!"
