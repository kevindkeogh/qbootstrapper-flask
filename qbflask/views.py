#!/usr/bin/python3

from flask import request, render_template
from qbflask import app
from qbflask.forms import InstrumentList
import qbflask.bootstrapper as bstrap

@app.route('/', methods=['GET'])
def index():
    form = InstrumentList()
    return render_template('index.html', form=form)

@app.route('/build_curve', methods=['POST'])
def build_curve():
    data = bstrap.parse_form(request.form)
    return render_template('build_curve.html', data=data)
