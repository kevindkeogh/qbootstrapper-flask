#!/usr/bin/python3

from datetime import datetime as dt
from flask import request, render_template, jsonify
from numpy import exp
from qbflask import app
from qbflask.forms import InstrumentList, Convention
from qbflask.bootstrapper import build_curve, validate
from qbflask.models import get_db


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


@app.route('/conventions', methods=['GET', 'POST'])
def curve_conventions():
    '''

    Note that this returns the entire db of conventions, to save from having
    to make multiple POST requests every time a currency (or instrument) is
    changed.
    '''
    if request.method == 'GET':
        form = Convention()
        return render_template('conventions.html', form=form)
    elif request.method == 'POST':
        # Needs to be updated. Right now it only returns the conventions in
        # the db, it should be able to accept new conventions and add them
        db = get_db()
        cur = db.cursor()
        query = 'SELECT name, currency, instrument, convention FROM CONVENTIONS'
        cur.execute(query)
        conventions = {}
        for row in cur:
            # Note that this creates a dict of convention.currency.name = JSON
            if row['currency'] not in conventions:
                conventions[row['currency']] = {}
            if row['instrument'] not in conventions[row['currency']]:
                conventions[row['currency']][row['instrument']] = {}
            conventions[row['currency']][row['instrument']][row['name']] = row['convention']
        return jsonify(conventions)


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
