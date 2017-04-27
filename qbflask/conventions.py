#!/usr/bin/python3
'''Functions and constants for all conventions, including adding and returning
lists of conventions
'''


import qbflask.models as models
import json
import re


INSTRUMENT_TYPES = [('OISCashRate', 'OIS Cash Rate'),
                    ('OISSwap', 'OIS Swap'),
                    ('LIBORCashRate', 'LIBOR Cash Rate'),
                    ('LIBORFuture', 'LIBOR Future'),
                    ('LIBORFRA', 'LIBOR FRA'),
                    ('LIBORSwap', 'LIBOR Swap Rate')]

CURVE_TYPES = [('OIS', 'OIS'), ('LIBOR', 'LIBOR')]

FREQ_TYPES = [('months', 'Months'), ('weeks', 'Weeks'), ('days', 'Days')]

ADJ_TYPES = [('unadjusted', 'Unadjusted'), ('following', 'Following'),
             ('modified following', 'Modified Following'),
             ('preceding', 'Preceding')]

BASIS_TYPES = [('act360', 'Actual/360'), ('act365', 'Actual/365'),
               ('30360', '30/360'), ('30E360', '30/360E')]

def add_convention(raw_data):
    '''Takes a flask request JSON object, calls the parser, and adds the
    information to the database
    '''
    try:
        data = parse_convs_form(raw_data)
        name = data['conv_name']
        ccy = data['currency']
        inst = data['conv_instrument_type']
        conv = json.dumps(data)
        db = models.get_db()
        cur = db.cursor()
        query = ('INSERT INTO CONVENTIONS(name, currency, instrument, '
                 'convention) VALUES(?, ?, ?, ?)')
        cur.execute(query, (name, ccy, inst, conv))
        db.commit()
        return (True, '{name} convention successfully added'.format(**locals()))
    except:
        return (False, 'An error occurred: {name} not added'.format(**locals()))


def parse_convs_form(raw_data):
    '''Takes Flask request JSON object and parses to dict for db addition'''
    convs = {}
    for row in raw_data:
        convs[row['name']] = row['value']
    return convs


def get_conventions_list():
    '''Returns nested dict of all conventions
        { Currency : { Instrument_type : [Name] } }
    '''
    db = models.get_db()
    cur = db.cursor()
    query = 'SELECT currency, instrument, name FROM CONVENTIONS'
    cur.execute(query)

    convs = {}
    for row in cur:
        if row['currency'] not in convs:
            convs[row['currency']] = {}
        if row['instrument'] not in convs[row['currency']]:
            convs[row['currency']][row['instrument']] = []
        convs[row['currency']][row['instrument']].append(row['name'])

    return convs


def convs_validate(conv):
    '''
    '''
    pass


def get_convention(name, currency):
    '''Gets a single convention from the database. Returns a python dict of
    conventions and strings
    '''
    db = models.get_db()
    cur = db.cursor()
    query = 'SELECT convention FROM conventions WHERE (name=? AND currency=?)'
    cur.execute(query, (name, currency))
    conv = cur.fetchone()[0]
    conv = json.loads(conv)
    return conv
