#!/usr/bin/python3

from datetime import datetime as dt
from flask import request, render_template, jsonify
from numpy import exp
from qbflask import app
from qbflask.forms import InstrumentList
from qbflask.bootstrapper import build_curve

@app.route('/', methods=['GET'])
def index():
    '''
    '''
    form = InstrumentList()
    return render_template('index.html', form=form)

@app.route('/curve', methods=['POST'])
def display_curve():
    '''
    '''
    curve = build_curve(request.json)
    dates = []
    for date in curve.curve['maturity']:
        dates.append(dt.strftime(date.astype(object), '%Y-%m-%d'))
    dfs = exp(curve.curve['discount_factor']).tolist()
    return jsonify(dates=dates, dfs=dfs)
