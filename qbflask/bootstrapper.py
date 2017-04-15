#!/usr/bin/python3
'''
'''

import datetime as dt
from dateutil.relativedelta import relativedelta
import qbootstrapper as qb
import re


def build_curve(jsondata):
    '''Main function to parse JSON object and return curve object'''
    data = parse_form(jsondata)
    curve_date = dt.datetime.strptime(data['curve_date'], '%Y-%m-%d')
    if data['curve_type'] == 'OIS':
        curve = qb.OISCurve(curve_date)
    elif data['curve_type'] == 'LIBOR':
        curve = qb.LIBORCurve(curve_date)
    insts = create_instruments(data, curve)
    curve.instruments = insts
    curve.build()
    return curve


def parse_form(jsondata):
    '''Takes Flask request JSON object and parses to dict for bootstrapping'''
    insts = {}
    insts['insts'] = {}
    for row in jsondata:
        if row['value'] == '': continue # skip if the value is nothing
        num = re.sub('\D', '', row['name']) # parse the string for digits
        try:
            num = int(num) # this might be a ValueError if not a number
            if num not in insts['insts']: insts['insts'][num] = {}
            term = row['name'].split('-')[-1]
            insts['insts'][num][term] = row['value']
        except ValueError:
            insts[row['name']] = row['value']
    return insts


def create_instruments(data, curve):
    '''Takes a dict of request information and returns a list of instruments'''
    instruments = []
    curve_date = dt.datetime.strptime(data['curve_date'], '%Y-%m-%d')
    for num, inst in data['insts'].items():
        maturity = dt.datetime.strptime(inst['maturity'], '%Y-%m-%d')
        rate = float(inst['rate']) / 100
        inst_type = inst['instrument_type']
        if inst_type == 'OISCashRate' or inst_type == 'LIBORCashRate':
            length_type, length_period = get_length(curve_date, maturity)
            instrument = qb.LIBORInstrument(curve_date, rate, length_period,
                                            curve, length_type=length_type)
        elif inst_type == 'OISSwap':
            instrument = qb.OISSwapInstrument(curve_date, maturity, rate, curve)
        elif inst_type == 'LIBORFuture':
            # Futures are assumed to be all 3m
            start_date = maturity - relativedelta(months=3)
            price = 100 - (rate * 100)
            instrument = qb.FuturesInstrumentByDates(start_date, maturity,
                                                     price, curve)
        elif inst_type == 'LIBORFRA':
            # FRAs are assumed to be all 6m
            start_date = maturity - relativedelta(months=6)
            instrument = qb.FRAInstrumentByDates(start_date, maturity, rate,
                                                 curve)
        elif inst_type == 'LIBORSwap':
            instrument = qb.LIBORSwapInstrument(curve_date, maturity, rate, curve)
        instruments.append(instrument)
    return [i for i in instruments if i is not None]


def get_length(effective, maturity):
    '''Heuristic for determining the proper period and length for cash insts'''
    num_days = (maturity - effective).days
    if (num_days > 30):
        length_type = 'months'
        length_period = num_days // 30
    elif (num_days > 7):
        length_type = 'weeks'
        length_period = num_days // 7
    else:
        length_type = 'days'
        length_period = num_days
    return (length_type, length_period)

def validate(req):
    '''Check curve request input params to ensure they are consistent

    Note that the response is a 2 element tuple. The first element is a Boolean
    for validity (true if valid, false is invalid) and the second is the first
    error failed or None if no error'''
    # Check the curve date works
    data = parse_form(req.json)
    try:
        curve_date = dt.datetime.strptime(data['curve_date'], '%Y-%m-%d')
    except KeyError:
        return (False, 'Curve date not entered')
    except ValueError:
        return (False, 'Curve date not recognized')
    except:
        return (False, 'Unexpected error in curve date')

    # Check that we have enough instruments
    if len(data['insts'].keys()) < 3:
        return (False, 'Must have at least 3 instruments')

    # Check if two instruments have the same maturity
    mats = [ i['maturity'] for i in data['insts'].values() ]
    if len(set(mats)) != len(mats):
        inst_nums = []
        inst_mats= []
        for num, inst in data['insts'].items():
            if inst['maturity'] in inst_mats:
                other_inst = inst_nums[inst_mats.index(inst['maturity'])]
                break
            else:
                inst_nums.append(num)
                inst_mats.append(inst['maturity'])
        return (False, 'Instrument {other_inst} and Instrument {num} have '
                       'the same maturity'.format(**locals()))

    cash_rate = False
    before = False
    for num, inst in data['insts'].items():
        # Check that we have at least 1 cash instrument
        if 'cash' in inst['instrument_type'].lower():
            cash_rate = True
        # Check that the maturities conform and are after the curve date
        try:
            mat = dt.datetime.strptime(inst['maturity'], '%Y-%m-%d')
        except KeyError:
            return (False,
                    'Instrument {num} maturity '
                    'not entered'.format(**locals()))
        except ValueError:
            return (False,
                    'Instrument {num} maturity '
                    'not recognized'.format(**locals()))
        except:
            return (False, 'Unexpected error in '
                           'Instrument {num} maturity'.format(**locals()))
        if mat < curve_date:
            before = True
            break # exit immediately, because there's an error

        # Check that the rates are numbers
        try:
            rate = float(inst['rate'])
        except ValueError:
            return (False, 'Instrument {num} rate '
                           'was not recognized'.format(**locals()))
        except:
            return (False, 'Unexpected error in '
                           'Instrument {num} rate'.format(**locals()))


    if not cash_rate:
        return (False, 'Must have at least 1 cash instrument')
    if before:
        return (False,
                'Instrument {num} maturity '
                'must be after the curve date'.format(**locals()))

    return (True, None)
