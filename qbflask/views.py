#!/usr/bin/python3

from flask import request, render_template
import numpy as np
from qbflask import app
from qbflask.forms import InstrumentList
from qbflask.bootstrapper import build_curve

@app.route('/', methods=['GET'])
def index():
    form = InstrumentList()
    return render_template('index.html', form=form)

@app.route('/curve', methods=['POST'])
def display_curve():
    curve = build_curve(request.form)
    dates = curve.curve['maturity']
    dfs = np.exp(curve.curve['discount_factor'])
    return render_template('curve.html', dates=dates, dfs=dfs)
