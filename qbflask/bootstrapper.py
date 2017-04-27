#!/usr/bin/python3
'''This modules handles all the processing of information to bootstrap the curve
'''

import datetime as dt
from dateutil.relativedelta import relativedelta
import qbootstrapper as qb
import qbflask.conventions as conventions
import re


def build_curve(raw_data):
    '''Main function to parse JSON object and return curve object
    '''
    data = parse_rates_form(raw_data)
    curve_date = dt.datetime.strptime(data['curve_date'], '%Y-%m-%d')
    if data['curve_type'] == 'OIS':
        curve = qb.OISCurve(curve_date)
    elif data['curve_type'] == 'LIBOR':
        curve = qb.LIBORCurve(curve_date)
    insts = create_instruments(data, curve)
    curve.instruments = insts
    curve.build()
    return curve


def parse_rates_form(raw_data):
    '''Takes Flask request JSON object and parses to dict for bootstrapping
    '''
    insts = {}
    insts['insts'] = {}
    for row in raw_data:
        if row['value'] == '':
            continue  # skip if the value is nothing
        num = re.sub('\D', '', row['name'])  # parse the string for digits
        try:
            num = int(num)  # this might be a ValueError if not a number
            if num not in insts['insts']:
                insts['insts'][num] = {}
            term = row['name'].split('-')[-1]
            insts['insts'][num][term] = row['value']
        except ValueError:
            insts[row['name']] = row['value']
    return insts


def create_instruments(data, curve):
    '''Takes a dict of request information and returns a list of instruments
    '''
    instruments = []
    curve_date = dt.datetime.strptime(data['curve_date'], '%Y-%m-%d')
    for num, inst in data['insts'].items():
        maturity = dt.datetime.strptime(inst['maturity'], '%Y-%m-%d')
        rate = float(inst['rate']) / 100
        inst_type = inst['instrument_type']
        conv = conventions.get_convention(inst['convention'], data['currency'])
        if inst_type == 'OISCashRate' or inst_type == 'LIBORCashRate':
            length_type, length_period = get_length(curve_date, maturity)
            instrument = qb.LIBORInstrument(curve_date, rate, length_period,
                                            curve, length_type=length_type,
                                            basis=conv['rate_basis'])
        elif inst_type == 'OISSwap':
            instrument = qb.OISSwapInstrument(curve_date, maturity, rate, curve,
                    rate_basis=conv['rate_basis'],
                    rate_period=int(conv['rate_length']),
                    rate_period_length=conv['rate_length_type'],

                    fixed_basis=conv['fixed_basis'],
                    fixed_length=int(conv['fixed_freq']),
                    fixed_period_length=conv['fixed_freq_length'],
                    fixed_period_adjustment=conv['fixed_period_adj'],
                    fixed_payment_adjustment=conv['fixed_payment_adj'],

                    float_basis=conv['float_basis'],
                    float_length=int(conv['float_freq']),
                    float_period_length=conv['float_freq_length'],
                    float_period_adjustment=conv['float_period_adj'],
                    float_payment_adjustment=conv['float_payment_adj']
                    )
        elif inst_type == 'LIBORFuture':
            rate_length = int(conv['rate_length'])
            if conv['rate_length_type'] == 'months':
                delta = relativedelta(months=rate_length)
            elif conv['rate_length_type'] == 'weeks':
                delta = relativedelta(weeks=rate_length)
            elif conv['rate_length_type'] == 'days':
                delta = relativedelta(days=rate_length)
            start_date = maturity - delta
            price = 100 - (rate * 100)
            instrument = qb.FuturesInstrumentByDates(start_date, maturity,
                                                     price, curve,
                                                     basis=conv['rate_basis'])
        elif inst_type == 'LIBORFRA':
            rate_length = int(conv['rate_length'])
            if conv['rate_length_type'] == 'months':
                delta = relativedelta(months=rate_length)
            elif conv['rate_length_type'] == 'weeks':
                delta = relativedelta(weeks=rate_length)
            elif conv['rate_length_type'] == 'days':
                delta = relativedelta(days=rate_length)
            start_date = maturity - delta
            instrument = qb.FRAInstrumentByDates(start_date, maturity, rate,
                                                 curve,
                                                 basis=conv['rate_basis'])
        elif inst_type == 'LIBORSwap':
            instrument = qb.LIBORSwapInstrument(curve_date, maturity, rate, curve,
                    rate_basis=conv['rate_basis'],
                    rate_period=int(conv['rate_length']),
                    rate_period_length=conv['rate_length_type'],

                    fixed_basis=conv['fixed_basis'],
                    fixed_length=int(conv['fixed_freq']),
                    fixed_period_length=conv['fixed_freq_length'],
                    fixed_period_adjustment=conv['fixed_period_adj'],
                    fixed_payment_adjustment=conv['fixed_payment_adj'],

                    float_basis=conv['float_basis'],
                    float_length=int(conv['float_freq']),
                    float_period_length=conv['float_freq_length'],
                    float_period_adjustment=conv['float_period_adj'],
                    float_payment_adjustment=conv['float_payment_adj']
                    )
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


def insts_validate(req):
    '''Check curve request input params to ensure they are consistent

    Note that the response is a 2 element tuple. The first element is a Boolean
    for validity (true if valid, false is invalid) and the second is the first
    error failed or None if no error'''
    # Check the curve date works
    data = parse_rates_form(req.json)
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
    mats = [i['maturity'] for i in data['insts'].values()]
    if len(set(mats)) != len(mats):
        inst_nums = []
        inst_mats = []
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
            break  # exit immediately, because there's an error

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
