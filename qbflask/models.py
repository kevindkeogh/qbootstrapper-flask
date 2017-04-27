#!/usr/bin/python3
'''Handles all database interactions for qbootstrapper
'''

from flask import g
from qbflask import app
import sqlite3


def connect_db():
    '''Connects to the database and returns the connection
    '''
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    '''Connects to the database and returns the connection

    Note that it ensures that the 'g' object holds a connection to the database
    '''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    '''Ensures that when a request is completed, the connection to the database
    is closed
    '''
    if hasattr(g, 'db'):
        g.db.close()


def init_db():
    '''Creates the database from scratch
    '''
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    '''Flask command to initialize the database (and tables)
    '''
    init_db()
    print('Initialized the database')
