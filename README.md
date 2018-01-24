# tozti

![documentation](https://readthedocs.org/projects/pip/badge/?version=latest)
[![build](https://www.travis-ci.org/tozti/tozti.svg?branch=master)](https://travis-ci.org/tozti/tozti)

This repository contains the core of the **tozti** software project. It is licensed
under the AGPLv3. See [documentation](https://tozti.readthedocs.io/en/latest/)
for more information.


## Quickstart

### Dependencies

For this project to work you will need:
- nodejs
- python3

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
The repository for this documentation is https://github.com/tozti/docs.

## Tests

### Launching tests

Tozti contains some tests. For them to be run, you need/
- to have installed the dependencies in `requirements-dev.txt`: `pip install -r requirements-dev.txt`
- to have either installed `chrome-driver` or `geckodriver` (for headerless web browser testing)

The test suite can be launched as:
```
pytest tests/ -driver [Chrome|Firefox]
```
If you are using `geckodriver`, user `Firefox` driver. Otherwise use `Chrome`

### Adding tests:

You can put extensions that are part of your testsuits inside `tests/extensions`. Not that you must add the build results inside them, so that travis doesn't have to rebuild the extensions everytime. Note that adding an extension inside this folder doesn't mean it will be tester: you must write the logic of the test inside a python script in `tests/`.
