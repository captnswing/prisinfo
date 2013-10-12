#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from parse_prisfil import get_prisfil_data, UnicodeDictReader

# configuration
DEBUG = True

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

@app.route("/")
def hello():
    entries = sorted(get_prisfil_data(cached=True))
    return render_template('prisfil.html', entries=entries)

if __name__ == "__main__":
    app.run()
