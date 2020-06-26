#!/usr/bin/env python3
import sys
import uuid
import argparse
import requests
from service_registry.orm.models import URL
from service_registry.orm import init_db, get_session


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser('Run service registry')
    parser.add_argument('--database', default="./data/services.sqlite")
    parser.add_argument('name', type=str)
    parser.add_argument('url', type=str)
    args = parser.parse_args(args)

    if not validate_url(args.url):
        print(f"{args.url} validation failed", file=sys.stderr, flush=True)
        sys.exit(1)

    init_db(uri="sqlite:///"+args.database)
    db_session = get_session()

    new_url = URL(url=args.url, name=args.name, id=uuid.uuid4())
    db_session.add(new_url)
    db_session.commit()


def validate_url(url):
    """
    Return True iff <url> is a valid URL address.
    :param url: URL address to be validated
    :return: bool
    """
    valid = False
    try:
        print(repr(url))
        #url = "https://googwle.com:81"
        print(url)
        print(type(url))
        print(len(url))
        requests.get(url, timeout=5)
        valid = True
    except requests.URLRequired:
        print("Invalid URL", file=sys.stderr, flush=True)
    except requests.TooManyRedirects:
        print("Too many redirects", file=sys.stderr, flush=True)
    except requests.exceptions.ConnectTimeout:
        print("Timeout occurred", file=sys.stderr, flush=True)
    except requests.ConnectionError as e:
        print("Unable to connect", file=sys.stderr, flush=True)
        print(e)
    except requests.RequestException as e:
        print("Unknown error", file=sys.stderr, flush=True)
        print(e)

    return valid


if __name__ == "__main__":
    main()
