"""
Unit test for all properties
Positive and Negative tests
"""

from unittest import TestCase

from encodingcom.encoding import Encoding


class EncodingPositive(TestCase):
    """
    Coverage for encoding.com positive tests
    """

    def setUp(self):
        """
        Setup a encoding.com object
        :return:
        """
        # TODO: Remove before release to Pypi
        self.encoding = Encoding('user_id', 'user_key')

    def tearDown(self):
        pass

    def test_add_media(self):
        """
        Test add media call
        :return:
        """
        pass


if __name__ == '__main__':
    from unittest import main

    main()
