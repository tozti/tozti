********************************
Install tozti in a computer room
********************************

As you do not have enough credentials in the computer rooms of the ENS to install node, npm and therefore tozti. Here is a step by step guide on how to make tozti works in the computer rooms.

The python part
===============

Tozti is divided in two parts:
- a python part
- a javascript part

For convenience, we use virtualenv to install the dependencies. But doing `python3 -m venv .venv` doesn't work in the computer rooms. However, `virtualenv` is installed.

Hence, the python's part of tozti's setup becomes::

    virtualenv -p python3 .venv
    . .venv/bin/activate
    pip3 install -r requirements.txt

The javascript part
===================

We need to install node and npm locally. Type the following command in your terminal::

    curl https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash

Restart your terminal and install node::

    nvm install node

Then go back to tozti's folder to install the js dependencies::

    npm install

And finally build tozti's js parts::

    npm run build

Launching tozti
===============

To run tozti it's the same as usual::

    python3 -m tozti dev
