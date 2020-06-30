"""
Unit tests for add_service.py.
"""
import sys
import unittest
import argparse
import add_service
from service_registry.orm.models import URL
from service_registry.orm import init_db, get_session


database = "./add_service_test.db"


class AddServiceTests(unittest.TestCase):
    """Unit tests for add_service.py."""
    def test_valid_url_200_response_code(self):
        """
        Test what happens when the URL is valid and the response code is 200.

        Note: Make sure that https://google.ca is up and running before you run this test.

        :return: None
        """
        valid = add_service.validate_url("https://google.ca")
        self.assertEqual(valid, True)

    def test_valid_url_non_200_response_code(self):
        """
        Test what happens when the URL is valid and the response code is not 200.

        Note: Make sure that https://httpstat.us is up and running before you run this test.

        :return: None
        """
        valid = add_service.validate_url("https://httpstat.us/404")
        self.assertEqual(valid, True)

    def test_valid_url_not_connectible(self):
        """
        Test what happens when the URL is valid but not connectible.

        Note: Make sure that https://httpstat.us is up and running before you run this test.

        :return: None
        """
        valid = add_service.validate_url("https://httpstat.us/200?sleep=10000")
        self.assertEqual(valid, False)

    def test_invalid_url(self):
        """
        Test what happens when the URL is invalid.

        Note: Make sure that https://sdjfafasdrhjweufhasdjkfhsjadkf.com is NOT a real URL before you run this test.
        If it does connect to an actual site, change it to a URL that is fake.

        :return: None
        """
        valid = add_service.validate_url("https://sdjfafasdrhjweufhasdjkfhsjadkf.com")
        self.assertEqual(valid, False)

    def test_add_url_not_in_db(self):
        """
        Test what happens when the URL to be added is not in the database.

        Note: Make sure that https://google.ca is up and running before you run this test.

        :return: None
        """
        init_db("sqlite:///" + database)
        db_session = get_session()
        db_session.query(URL).delete()
        db_session.commit()
        self.assertEqual(URL().query.filter_by(url='https://google.ca').count(), 0)
        add_service_args = ['--database', database, 'test', 'https://google.ca']
        add_service.main(add_service_args)
        self.assertEqual(URL().query.filter_by(url='https://google.ca').count(), 1)

    def test_add_url_already_in_db(self):
        """
        Test what happens when the URL to be added is already in the database.

        Note: Make sure that https://google.ca is up and running before you run this test.

        :return: None
        """
        init_db("sqlite:///" + database)
        db_session = get_session()
        db_session.query(URL).delete()
        db_session.commit()
        add_service_args = ['--database', database, 'test', 'https://google.ca']
        add_service.main(add_service_args)
        self.assertEqual(URL().query.filter_by(url='https://google.ca').count(), 1)
        add_service.main(add_service_args)
        self.assertEqual(URL().query.filter_by(url='https://google.ca').count(), 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run tests for add_service.py')
    parser.add_argument('--database', default=database)
    args = parser.parse_args()
    database = args.database
    del sys.argv[1:]
    unittest.main()
