#!/usr/bin/python3
'''
'''


import qbflask.models as models
import json
import re


def add_convention(raw_data):
    '''
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
    '''
    '''
    db = models.get_db()
    cur = db.cursor()
    query = 'SELECT convention FROM conventions WHERE (name=? AND currency=?)'
    cur.execute(query, (name, currency))
    conv = cur.fetchone()[0]
    conv = json.loads(conv)
    return conv
