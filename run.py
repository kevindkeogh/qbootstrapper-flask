#!/usr/bin/python3

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import wtforms as wtf

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='secret',
    USERNAME='admin',
    PASSWORD='admin'
))

class Instrument(wtf.Form):
    instrument_type = wtf.TextField('Instrument')
    expiry = wtf.DateField('Expiry')
    rate = wtf.DecimalField('Rate')

class InstrumentList(wtf.Form):
    instruments = wtf.FieldList(wtf.FormField(Instrument), min_entries=3)
    submit = wtf.SubmitField('Submit')

@app.route('/')
def index():
    form = InstrumentList()
    # raise
    return render_template('index.html', form=form)

@app.route('/build_curve.html')
def build_curve():
    return "Hello!"

if __name__ == '__main__':
    app.run()
