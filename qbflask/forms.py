#!/usr/bin/python3

import wtforms as wtf

class Instrument(wtf.Form):
    instrument_type = wtf.TextField('Instrument')
    expiry = wtf.DateField('Expiry')
    rate = wtf.DecimalField('Rate')

class InstrumentList(wtf.Form):
    instruments = wtf.FieldList(wtf.FormField(Instrument), min_entries=3)
    submit = wtf.SubmitField()
