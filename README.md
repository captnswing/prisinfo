# Prisinfo

## Mission

compare prices for all products in magento_prisfil with prices on pricerunner, prisjakt, kelkoo, etc.

## Installation

### install the prerequisits

To run the scripts in this project, you'll need `git`, `python2.7`, `setuptools`, `pip` and `virtualenvwrapper`.

###### install git

    curl -O https://git-osx-installer.googlecode.com/files/git-1.8.3.2-intel-universal-snow-leopard.dmg
    hdid git-1.8.3.2-intel-universal-snow-leopard.dmg
    sudo installer -target '/' -pkg /Volumes/Git\ 1.8.3.2\ Snow\ Leopard\ Intel\ Universal/git-1.8.3.2-intel-universal-snow-leopard.pkg
    diskutil eject /Volumes/Git\ 1.8.3.2\ Snow\ Leopard\ Intel\ Universal
    rm git-1.8.3.2-intel-universal-snow-leopard.dmg

###### install python 2.7

Make sure that the installed python version is >2.7. This should be the case on all Mac OS X versions >= 10.8 (Mountain Lion).

Open a Terminal window. The command

	python --version

should output something like

	Python 2.7.2

###### install setuptools

	curl -O https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
	sudo python ez_setup.py
	rm ez_setup.py

###### install pip

	curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
	sudo python get-pip.py
	rm get-pip.py

###### install virtualenvwrapper

	sudo pip install virtualenvwrapper

Append the following to your shell startup file

	export WORKON_HOME=$HOME/.virtualenvs
	source `which virtualenvwrapper.sh`

### install the project

Now you should be able to create a virtualenv for this project

	mkvirtualenv prisinfo

Check out the project

	cd ~/Development
	git clone https://github.com/captnswing/prisinfo.git

## Running the script

In the Terminal

	workon prisinfo
	cd ~/Development/prisinfo
	./parse_prisfil.py
