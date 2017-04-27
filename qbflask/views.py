#!/usr/bin/python3

from datetime import datetime as dt
from flask import request, render_template, jsonify
from numpy import exp
from qbflask import app
import qbflask.bootstrapper as bstrap
import qbflask.conventions as conv
from qbflask.forms import InstrumentList, Convention
from qbflask.models import get_db


@app.route('/', methods=['GET'])
def index():
    '''
    '''
    form = InstrumentList()
    return render_template('index.html', form=form)


@app.route('/conventions', methods=['GET'])
def conventions():
    '''

    Note that this returns the entire db of conventions, to save from having
    to make multiple POST requests every time a currency (or instrument) is
    changed.
    '''
    if request.method == 'GET':
        form = Convention()
        return render_template('conventions.html', form=form)


@app.route('/api/v1/bootstrap', methods=['POST'])
def bootstrap_curve():
    '''
    '''
    valid, reason = bstrap.insts_validate(request)
    if not valid:
        return unacceptable_input(reason)
    curve = bstrap.build_curve(request.json)
    dates = []
    for date in curve.curve['maturity']:
        dates.append(dt.strftime(date.astype(object), '%Y-%m-%d'))
    dfs = exp(curve.curve['discount_factor']).tolist()
    return jsonify(dates=dates, dfs=dfs)


@app.route('/api/v1/conventions/add', methods=['POST'])
def add_convention():
    '''
    '''
    success, status = conv.add_convention(request.json)
    if success:
        return (status, 200)
    else:
        return (status, 400)


@app.route('/api/v1/conventions/get', methods=['GET'])
def get_conventions():
    '''
    '''
    convs = conv.get_conventions_list()
    return jsonify(convs)


@app.errorhandler(406)
def unacceptable_input(error="Unknown error"):
    '''
    '''
    message = {
               'status': 406,
               'message': 'Inputs unacceptable: ' + error
              }
    resp = jsonify(message)
    resp.status_code = 406
    return resp
