#!/usr/bin/python3
'''
'''

from flask import g
from qbflask import app
import sqlite3


def connect_db():
    '''
    '''
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    '''
    '''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    '''
    '''
    if hasattr(g, 'db'):
        g.db.close()


def init_db():
    '''
    '''
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    '''
    '''
    init_db()
    print('Initialized the database')
