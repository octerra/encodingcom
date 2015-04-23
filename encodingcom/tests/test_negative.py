"""
Unit test for all properties
Positive and Negative tests
"""

from unittest import TestCase

from encoding import Encoding
from exception import GenericError


class EncodingNegative(TestCase):
    """
    Coverage for encoding.com positive tests
    """

    def setUp(self):
        """
        Setup a encoding.com object
        :return:
        """
        # TODO: Remove before release to Pypi
        self.encoding = Encoding('33524', '151ff24e4fcf5f18b33468d129bd36c7')

    def tearDown(self):
        pass

    def test_get_media_info(self):
        """
        Test get media info with bad parameters
        * Missing media id from client
        * Invalid media id not found

        :return:
        """
        with self.assertRaises(GenericError):
            self.encoding.get_media_info(mediaid=[])
            self.encoding.get_media_info(mediaid=['1', '2'])


if __name__ == '__main__':
    from unittest import main

    main()
