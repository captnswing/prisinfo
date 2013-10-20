#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from prisfilparser import get_prisfil_data
import os
from datetime import datetime
from settings import PRISFIL_CACHED, CURRENCY_SYMBOL, CURRENCY_THOUSAND_SEPARATOR
from util import humanize_date_difference


# configuration
DEBUG = True

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)


@app.route("/")
def prisfil():
    entries = sorted(get_prisfil_data())
    prisfil_date = datetime.fromtimestamp(os.path.getmtime(PRISFIL_CACHED))
    print prisfil_date
    date_difference = humanize_date_difference(prisfil_date, datetime.now())
    print date_difference
    return render_template('prisfil.html',
                           entries=entries,
                           prisfil_date=prisfil_date,
                           date_difference=date_difference.replace(' ago', '')
    )


@app.context_processor
def utility_processor():
    def format_price(amount, currency=CURRENCY_SYMBOL):
        return u'{0:,.0f} {1}'.format(amount, currency) \
            .replace(',', CURRENCY_THOUSAND_SEPARATOR)

    return dict(format_price=format_price)


if __name__ == "__main__":
    app.run()
