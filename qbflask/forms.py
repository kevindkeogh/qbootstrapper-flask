#!/usr/bin/python3

import wtforms as wtf

INSTRUMENT_TYPES = [('OISSwap', 'OIS Swap'), ('OISCashRate', 'OIS Cash Rate')]

class Instrument(wtf.Form):
    instrument_type = wtf.SelectField('Instrument', choices=INSTRUMENT_TYPES)
    expiry = wtf.DateField('Expiry', '%Y-%m-%d')
    rate = wtf.DecimalField('Rate')

class InstrumentList(wtf.Form):
    instruments = wtf.FieldList(wtf.FormField(Instrument), min_entries=3)
    submit = wtf.SubmitField()
