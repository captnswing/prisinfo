# Prisinfo

## Mission

compare prices for all products in magento_prisfil with prices on pricerunner, prisjakt, kelkoo, etc.

## Installation

To run the scripts in this project, you'll need `python2.7`, `setuptools`, `pip` and `virtualenvwrapper`.

Make sure that the installed python version is >2.7. This should be the case on all Mac OS X versions >= 10.8 (Mountain Lion).

Open a Terminal window. The command

	python --version

should output something like

	Python 2.7.2

Then, install setuptools

	curl -O https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
	sudo python ez_setup.py
	rm ez_setup.py

Then, install pip

	curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
	sudo python get-pip.py
	rm get-pip.py

Then, install virtualenvwrapper

	sudo pip install virtualenvwrapper

Append the following to your shell startup file

	export WORKON_HOME=$HOME/.virtualenvs
	source /usr/local/bin/virtualenvwrapper.sh

Now you should be able to create a virtualenv for this project

	mkvirtualenv prisinfo

Check out this project

	cd ~/Development
	git clone git@github.com:captnswing/prisinfo.git

## Running the script(s)

In the Terminal

	workon prisinfo
	cd ~/Development/prisinfo
	./parse_prisfil.py
