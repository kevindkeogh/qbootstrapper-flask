#!/usr/bin/python3
'''
'''

import wtforms as wtf
import wtforms.fields.html5 as wtffields

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


class Instrument(wtf.Form):
    '''
    '''
    instrument_type = wtf.SelectField('Instrument', choices=INSTRUMENT_TYPES)
    maturity = wtffields.DateField('Maturity', '%Y-%m-%d')
    rate = wtf.TextField('Rate')
    convention = wtf.SelectField('Convention', choices=[('none', '')])


class InstrumentList(wtf.Form):
    '''
    '''
    curve_date = wtffields.DateField('Curve date')
    curve_type = wtf.SelectField('Curve type', choices=CURVE_TYPES)
    currency = wtf.TextField('Currency')
    instruments = wtf.FieldList(wtf.FormField(Instrument), min_entries=3)
    submit = wtf.SubmitField()


class Convention(wtf.Form):
    conv_name = wtf.TextField('Name')
    currency = wtf.TextField('Currency')
    conv_instrument_type = wtf.SelectField('Instrument Type', choices=INSTRUMENT_TYPES)
    submit = wtf.SubmitField()
    # Cash conventions
    rate_basis = wtf.SelectField('Rate Basis', choices=BASIS_TYPES)
    rate_length = wtf.TextField('Length')
    rate_length_type = wtf.SelectField('Length Type', choices=FREQ_TYPES)
    # Futures conventions - same as cash
    # FRA conventions - same as cash
    # Swap Conventions
    #  Fixed leg
    fixed_basis = wtf.SelectField('Fixed Basis', choices=BASIS_TYPES)
    fixed_freq = wtf.TextField('Fixed Frequency')
    fixed_freq_length = wtf.SelectField('Fixed Frequency Type', choices=FREQ_TYPES)
    fixed_period_adj = wtf.SelectField('Fixed Period Adjustment', choices=ADJ_TYPES)
    fixed_payment_adj = wtf.SelectField('Fixed Payment Adjustment', choices=ADJ_TYPES)
    #  Float leg
    float_basis = wtf.SelectField('Float Basis', choices=BASIS_TYPES)
    float_freq = wtf.TextField('Float Frequency')
    float_freq_length = wtf.SelectField('Float Frequency Type', choices=FREQ_TYPES)
    float_period_adj = wtf.SelectField('Float Period Adjustment', choices=ADJ_TYPES)
    float_payment_adj = wtf.SelectField('Float Payment Adjustment', choices=ADJ_TYPES)
    # For rate basis, leave the cash conventions minus the payment adj
