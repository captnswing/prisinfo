#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from prisfilparser import get_prisfil_data
import os
import time
from settings import PRISFIL_CACHED, CURRENCY_SYMBOL, CURRENCY_THOUSAND_SEPARATOR

# configuration
DEBUG = True

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

@app.route("/")
def prisfil():
    entries = sorted(get_prisfil_data())
    prisfil_date = time.ctime(os.path.getmtime(PRISFIL_CACHED))
    return render_template('prisfil.html', entries=entries, prisfil_date=prisfil_date)

def format_currency(value):
    return '{:,.0f} {:s}'.format(value, CURRENCY_SYMBOL)\
                         .replace(',', CURRENCY_THOUSAND_SEPARATOR)

app.jinja_env.filters['format_currency'] = format_currency

if __name__ == "__main__":
    app.run()
