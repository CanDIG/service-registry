# Service Registry

[![Build Status](https://travis-ci.com/ljdursi/service-registry.svg?branch=trunk)](https://travis-ci.com/ljdursi/service-registry)
[![CodeFactor](https://www.codefactor.io/repository/github/ljdursi/service-registry/badge)](https://www.codefactor.io/repository/github/ljdursi/service-registry)
[![PyUp](https://pyup.io/repos/github/ljdursi/service-registry/shield.svg)](https://pyup.io/repos/github/ljdursi/service-registry/)
[![Quay.io](https://quay.io/repository/ljdursi/service-registry/status)](https://quay.io/repository/ljdursi/service-registry)

## Stack

- [Connexion](https://github.com/zalando/connexion) for implementing the API
- [SQLAlchemy](http://sqlalchemy.org), using [Sqlite3](https://www.sqlite.org/index.html) for ORM
- [Dredd](https://dredd.readthedocs.io/en/latest/) and [Dredd-Hooks-Python](https://github.com/apiaryio/dredd-hooks-python) for testing
- Python 3.7+
- Pytest, tox
- [Travis CI](https://travis-ci.org/)

## Installation

The server software can be installed in a virtual environment:

```
pip install -r requirements.txt
pip install -r requirements_dev.txt
python3 setup.py develop
```

For automated testing you can install Dredd. Assuming you already have Node and npm installed:

```
npm install -g dredd
```

### Running

The server can be run with:

```
python3 -m service_registry
```

There are several command line arguments you can pass in when running the server:

`--database` Path to the database. Default path is `./data/services.sqlite`.

`--host` Hostname for where this application is running. Default hostname is `localhost`.

`--port` Port on which this application is running. Default port is `3000`.

`--logfile` Path to the log file. Default path is `./log/services.log`.

`--loglevel` Verbosity of the logging. Must be one of `{'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'}`. Default is `INFO`.

`--remove-active` When this argument is given, the `active` field is not shown in responses. By default,
the `active` field is shown in responses.

After starting up the server, sending a request to `host:port` (`localhost:3000` by default) should give you the following response:

```

```

There are a few endpoints:

`/services` Returns a list consisting of each service's information.

`/services/types` Returns a list of all the service types.

`/services/{serviceID}` Returns service information for the service with ID `serviceID`.

`/service-info` Returns service information for this application.

Before you can get a useful response from the first three endpoints, you need to add the services you want the application to
look at:

```
python3 -m add_service "ELIXIR Beacon FI" "https://staging-elixirbeacon.rahtiapp.fi"
```

There are a few command line arguments to be aware of when adding a service:

`--database` Path to the database to add the service to. Default path is `./data/services.sqlite`.

`name` Name of the service being added. The first string in the command is the name of the service.

`url` URL of the service being added. The second string in the command is the URL of the service.

Without adding any services, sending a request to `/services` will return the following response:

```
[]
```

Adding a service:

```
python3 -m add_service "ELIXIR Beacon FI" "https://staging-elixirbeacon.rahtiapp.fi"
```

Now, sending a request to `/services` will return a response similar to:

```

```

For testing, the Dredd config is currently set up to launch the service itself, so no server needs to be running:

```
cd tests
dredd --hookfiles=dreddhooks.py
```
