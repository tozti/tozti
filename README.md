# tozti

![documentation](https://readthedocs.org/projects/pip/badge/?version=latest)
[![build](https://www.travis-ci.org/tozti/tozti.svg?branch=master)](https://travis-ci.org/tozti/tozti)

This repository contains the core of the **tozti** software project. It is licensed
under the AGPLv3. See [documentation](https://tozti.readthedocs.io/en/latest/)
for more information.


## Quickstart

### Dependencies

For this project to work you will need:
- nodejs (>=9.4.0 garanteed, earlier versions may or may not work)
- python3 (>= 3.5)

### Installation

Start by creating a virtualenv and activate it:
```
python3 -m venv .venv
source .venv/bin/activate
```

The next step is to install tozti's python dependencies:
```
pip install -r requirements.txt
```

Finally, install the client-side dependencies and build the client code:
```
npm install
npm run build
```

### Lauching tozti

```
python3 -m tozti dev
```

### Installing extensions

To install an extension, simply copy the extension folder inside `extensions/`.
*Some extensions require an additional step to compile their client code, but it is their responsability to explain the build process*.

## Documentation

The documentation for **tozti** is available online on [tozti.readthedocs.io](https://tozti.readthedocs.io). 
It is build using [sphinx](http://www.sphinx-doc.org/en/stable/) from the files contained inside `docs`.

### Editing

The documentation is written in *reStructuredText* (reST) markup which is somewhat similar to markdown, but way more powerful. Take a look at the [cheatsheet](http://www.sphinx-doc.org/en/stable/rest.html) or the [specification](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html) for informations on how to use reST.

### Installing Sphinx

The Sphinx package is available on the PyPI, you can install it with the usual `pip --user install sphinx`. If you have multiple python versions installed replace `pip` with `python3 -m pip`; if you don't have pip installed on that python version, just run `python3 -m ensurepip` first.

### Building

Just issue `make html` inside the `docs` directory. The output will be inside `docs/_build/html`, you can view it locally by running `python3 -m http.server 8080` and browsing http://localhost:8080. Do *not* include output files in the repository, the documentation is being built automatically by readthedocs.


## Tests

### Launching tests

Tozti contains some tests. For them to be run, you need/
- to have installed the dependencies in `requirements-dev.txt`: `pip install -r requirements-dev.txt`
- to have either installed `chrome-driver` or `geckodriver` (for headerless web browser testing)

The test suite can be launched as:
```
pytest tests/ --driver [Chrome|Firefox]
```
If you are using `geckodriver`, user `Firefox` driver. Otherwise use `Chrome`

### Adding tests:

You can put extensions that are part of your testsuits inside `tests/extensions`. Not that you must add the build results inside them, so that travis doesn't have to rebuild the extensions everytime. Note that adding an extension inside this folder doesn't mean it will be tester: you must write the logic of the test inside a python script in `tests/`.
