#!/usr/bin/python3

from flask import request, session, g, redirect, url_for, abort, render_template, flash
from qbflask import app
from qbflask.forms import InstrumentList

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InstrumentList()
    if request.method == 'POST':
        pass
        # pprint.pprint(request.form)
    return render_template('index.html', form=form)

@app.route('/build_curve.html')
def build_curve():
    return "Hello!"
