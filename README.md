# Service Registry

[![Build Status](https://travis-ci.org/CanDIG/serice_registry.svg?branch=master)](https://travis-ci.org/CanDIG/serice_registry)
[![CodeFactor](https://www.codefactor.io/repository/github/CanDIG/serice_registry/badge)](https://www.codefactor.io/repository/github/CanDIG/serice_registry)
[![PyUp](https://pyup.io/repos/github/CanDIG/serice_registry/shield.svg)](https://pyup.io/repos/github/CanDIG/serice_registry/)
[![Quay.io](https://quay.io/repository/candig/serice_registry/status)](https://quay.io/repository/candig/serice_registry)

## Stack

- [Connexion](https://github.com/zalando/connexion) for implementing the API
- [SQLAlchemy](http://sqlalchemy.org), using [Sqlite3](https://www.sqlite.org/index.html) for ORM
- [Bravado-core](https://github.com/Yelp/bravado-core) for Python classes from the spec
- [Dredd](https://dredd.readthedocs.io/en/latest/) and [Dredd-Hooks-Python](https://github.com/apiaryio/dredd-hooks-python) for testing
- Python 3
- Pytest, tox
- Travis-CI

## Installation

The server software can be installed in a virtual environment:

```
pip install -r requirements.txt
pip install -r requirements_dev.txt
python setup.py develop
```

for automated testing you can install dredd; assuming you already have node and npm installed,

```
npm install -g dredd
```

### Running

The server can be run with, for instance

```
python3 -m serice_registry --database=test.db --logfile=test.log --loglevel=WARN
```

For testing, the dredd config is currently set up to launch the service itself, so no server needs be running:

```
cd tests
dredd --hookfiles=dreddhooks.py
```
