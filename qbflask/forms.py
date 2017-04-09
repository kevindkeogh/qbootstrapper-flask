#!/usr/bin/python3

import wtforms as wtf
import wtforms.fields.html5 as wtffields

INSTRUMENT_TYPES = [('OISSwap', 'OIS Swap'), ('OISCashRate', 'OIS Cash Rate')]

class Instrument(wtf.Form):
    instrument_type = wtf.SelectField('Instrument', choices=INSTRUMENT_TYPES)
    expiry = wtffields.DateField('Expiry', '%Y-%m-%d')
    rate = wtffields.DecimalField('Rate')

class InstrumentList(wtf.Form):
    instruments = wtf.FieldList(wtf.FormField(Instrument), min_entries=3)
    submit = wtf.SubmitField()
