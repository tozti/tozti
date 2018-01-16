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
