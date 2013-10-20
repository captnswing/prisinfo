# Prisinfo

## Mission

compare prices for all products in magento_prisfil with prices on pricerunner, prisjakt, kelkoo, etc.

## Installation

### install the prerequisits

This is documented in detail [on the wiki](https://github.com/captnswing/prisinfo/wiki/Install-prerequisits) now.

### install the project

After installing the prerequisits, you should be able to create a virtualenv for this project

	mkvirtualenv prisinfo

Then, check out the project code from github

	cd ~/Development
	git clone https://github.com/captnswing/prisinfo.git
	pip install -r requirements.txt

## Update the code

In the Terminal

	workon prisinfo
	cd ~/Development/prisinfo
	git pull
	pip install -r requirements.txt

## Running the application

### the parser script

In the Terminal

	workon prisinfo
	cd ~/Development/prisinfo
	./prisfilparser.py

### the admin GUI

In the Terminal

	workon prisinfo
	cd ~/Development/prisinfo
	python admin.py

Then, open a browser, and surf to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
