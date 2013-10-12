#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from parse_prisfil import get_prisfil_data, UnicodeDictReader

# configuration
#DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

@app.route("/")
def hello():
    entries = sorted(get_prisfil_data(cached=True))
    return render_template('show_entries.html', entries=entries)

if __name__ == "__main__":
    app.run()
