#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from parse_prisfil import get_prisfil_data
import os
from settings import PRISFIL_CACHED

# configuration
DEBUG = True

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

@app.route("/")
def prisfil():
    entries = sorted(get_prisfil_data())
    prisfil_date = os.path.getmtime(PRISFIL_CACHED)
    return render_template('prisfil.html', entries=entries, prisfil_date=prisfil_date)

def format_currency(value):
    return '{:,.0f} kr'.format(value).replace(',', ' ')

app.jinja_env.filters['format_currency'] = format_currency

if __name__ == "__main__":
    app.run()
