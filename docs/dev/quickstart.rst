**********
Quickstart
**********

To start working on tozti you only need python3 and git (you should be able
to install them from your package manager). Make sure you have at least python
3.5 (for the ``async/await`` syntax) and ``setuptools`` installed::

   python3 --version
   python3 -m ensurepip --upgrade  # may need root privileges

One good way to organize yourself is to create a ``tozti`` folder somewhere::

   mkdir tozti && cd tozti

A good practice when working on python projects is to setup a virtual
environnement (venv). A venv behaves much like a separated python installation:
it has it's own separated list of installed packages so that when you are
working on two projects that need different version of a specific package you
just put them in different venvs and install different versions on each. For
more informations see the :py:mod:`venv` module and :pep:`405`. You may
create a venv named ``venv`` inside the ``tozti`` folder with::

    python3 -m venv venv      # create it
    source venv/bin/activate  # activate it

Now that you are inside the venv (you should see ``(venv)`` at the beginning of
your prompt), the ``pip`` and ``python`` commands will be aliased to the ones
from the venv. To deactivate it just issue ``deactivate``. Now you can clone
the repos, install them inside your venv and start tozti::

   git clone git@github.com:tozti/tozti && cd tozti
   pip install -r requirements.txt
   python3 -m tozti dev  # from the root of the repo

Extensions are located inside the ``extensions`` folder. To build one, make
sure you have the ``npm`` package, then type::

   npm install    # only needed when you change package.json
   npm run build  # build the *.vue files to browser-compatible javascript


.. _python documentation: https://docs.python.org/3.6/library/venv.html
