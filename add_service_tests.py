import unittest
import argparse
import add_service


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

        Note: Make sure that https://sdjfafasdrhjweufhasdjkfhsjadkf.com is NOT a real URL. If it does connect to an
        actual site, change it to a URL that is fake.

        :return: None
        """
        valid = add_service.validate_url("https://sdjfafasdrhjweufhasdjkfhsjadkf.com")
        self.assertEqual(valid, False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run tests for add_service.py')
    parser.add_argument('--database', default="./test.db")
    args = parser.parse_args()
    database = args.database

    unittest.main()
