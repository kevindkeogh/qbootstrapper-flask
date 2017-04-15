#!/usr/bin/python3

from datetime import datetime as dt
from flask import request, render_template, jsonify
from numpy import exp
from qbflask import app
from qbflask.forms import InstrumentList
from qbflask.bootstrapper import build_curve, validate


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
    valid, reason = validate(request)
    if not valid:
        return unacceptable_input(reason)
    curve = build_curve(request.json)
    dates = []
    for date in curve.curve['maturity']:
        dates.append(dt.strftime(date.astype(object), '%Y-%m-%d'))
    dfs = exp(curve.curve['discount_factor']).tolist()
    return jsonify(dates=dates, dfs=dfs)


@app.errorhandler(406)
def unacceptable_input(error="Unacceptable input"):
    '''
    '''
    message = {
            'status': 406,
            'message': 'Inputs unacceptable: ' + error
            }
    resp = jsonify(message)
    resp.status_code = 406
    return resp
