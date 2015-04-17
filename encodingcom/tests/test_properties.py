"""
Unit test for all properties
Positive and Negative tests
"""

from unittest import TestCase

from exceptions import InvalidParameterError
from format import Format


class PropertyTests(TestCase):
    """
    Coverage for all properties
    """

    def setUp(self):
        """
        Setup a dummy Encoding service object
        :return:
        """
        self.format = Format()

    def tearDown(self):
        pass

    def test_positive_video_codec(self):
        """
        Test all the positive scenarios in video codec parameter
        :return:
        """
        try:
            # TODO: test and cross check all references against encoding.com settings
            test_settings = ['mov', 'mov:libx264']

            for setting in test_settings:
                self.format.video_codec = setting
        except:
            self.fail('Expected valid settings for video codec failed with an exception')

    def test_negative_video_codec(self):
        """
        Negative test cases for video codec
        * Invalid encoder:  'mov:bad_encoder
        * Invalid encoder type:  'invalid'

        :return:
        """
        with self.assertRaises(InvalidParameterError):
            self.format.video_codec = 'mov:bad_encoder'
        with self.assertRaises(InvalidParameterError):
            self.format.video_codec = 'invalid'


if __name__ == '__main__':
    from unittest import main

    main()
