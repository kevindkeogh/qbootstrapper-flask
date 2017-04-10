#!/usr/bin/python3

import datetime
import qbootstrapper as qb
import re

def build_curve(formdata):
    data = parse_form(formdata)
    curve_date = datetime.datetime.strptime(data['curve_date'], '%Y-%m-%d')
    if data['curve_type'] == 'OIS':
        curve = qb.OISCurve(curve_date)
    elif data['curve_type'] == 'LIBOR':
        curve = qb.LIBORCurve(curve_date)
    # else:
    #   TODO return error
    insts = create_instruments(data, curve)
    curve.instruments = insts
    curve.build()
    return curve


def parse_form(form):
    '''Takes Flask request object and parses to dict for bootstrapping'''
    insts = {}
    insts['insts'] = {}
    for key, value in form.items():
        if key == '': continue
        num = re.sub('\D', '', key)
        try:
            num = int(num) # this might be a ValueError if not a number
            if num not in insts['insts']: insts['insts'][num] = {}
            term = key.split('-')[-1]
            insts['insts'][num][term] = value
        except ValueError:
            insts[key] = value
    return insts


def create_instruments(data, curve):
    '''Takes a dict of request information and returns a list of instruments'''
    instruments = []
    curve_date = datetime.datetime.strptime(data['curve_date'], '%Y-%m-%d')
    for num, inst in data['insts'].items():
        maturity = datetime.datetime.strptime(inst['maturity'], '%Y-%m-%d')
        rate = float(inst['rate'])
        inst_type = inst['instrument_type']
        if inst_type == 'OISSwap':
            instrument = qb.OISSwapInstrument(curve_date, maturity, rate, curve)
        elif inst_type == 'OISCashRate':
            num_days = (maturity - curve_date).days
            instrument = qb.LIBORInstrument(curve_date, rate, num_days, curve,
                                            length_type='days')
        # TODO Add LIBOR instruments
        instruments.append(instrument)
    return instruments