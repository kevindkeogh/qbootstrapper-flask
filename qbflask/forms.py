#!/usr/bin/python3

import wtforms as wtf
import wtforms.fields.html5 as wtffields

INSTRUMENT_TYPES = [('OISCashRate', 'OIS Cash Rate'),
                    ('OISSwap', 'OIS Swap'),
                    ('LIBORCashRate', 'LIBOR Cash Rate'),
                    ('LIBORFuture', 'LIBOR Future'),
                    ('LIBORFRA', 'LIBOR FRA'),
                    ('LIBORSwap', 'LIBOR Swap Rate')]

CURVE_TYPES = [('OIS', 'OIS'), ('LIBOR', 'LIBOR')]

class Instrument(wtf.Form):
    instrument_type = wtf.SelectField('Instrument', choices=INSTRUMENT_TYPES)
    maturity = wtffields.DateField('Maturity', '%Y-%m-%d')
    rate = wtf.TextField('Rate')
    convention = wtf.SelectField('Convention', choices=[('none', '')])

class InstrumentList(wtf.Form):
    curve_date = wtffields.DateField('Curve date')
    curve_type = wtf.SelectField('Curve type', choices=CURVE_TYPES)
    currency = wtf.TextField('Currency')
    instruments = wtf.FieldList(wtf.FormField(Instrument), min_entries=3)
    submit = wtf.SubmitField(id='instruments-submit')
