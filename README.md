# Service Registry

[![Build Status](https://travis-ci.org/ljdursi/service-registry.svg?branch=master)](https://travis-ci.org/ljdursi/service-registry)
[![CodeFactor](https://www.codefactor.io/repository/github/ljdursi/service-registry/badge)](https://www.codefactor.io/repository/github/ljdursi/service-registry)
[![PyUp](https://pyup.io/repos/github/ljdursi/service-registry/shield.svg)](https://pyup.io/repos/github/ljdursi/service-registry/)
[![Quay.io](https://quay.io/repository/ljdursi/service-registry/status)](https://quay.io/repository/ljdursi/service-registry)

## Stack

- [Connexion](https://github.com/zalando/connexion) for implementing the API
- [SQLAlchemy](http://sqlalchemy.org), using [Sqlite3](https://www.sqlite.org/index.html) for ORM
- [Dredd](https://dredd.readthedocs.io/en/latest/) and [Dredd-Hooks-Python](https://github.com/apiaryio/dredd-hooks-python) for testing
- Python 3.7+
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
python3 -m service_registry --database=test.db --logfile=test.log --loglevel=WARN
```

For testing, the dredd config is currently set up to launch the service itself, so no server needs be running:

```
cd tests
dredd --hookfiles=dreddhooks.py
```
