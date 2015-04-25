"""
Unit test for all properties
Positive and Negative tests
"""

from unittest import TestCase

from encodingcom.encoding import Encoding
from encodingcom.exception import EncodingErrors

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
        self.encoding = Encoding('33524', '151ff24e4fcf5f18b33468d129bd36c7')

    def tearDown(self):
        pass

    def test_add_media(self):
        """
        Test add media call
        :return:
        """

        mp4_libx264 = {'output': 'mp4', 'video_codec': 'libx264'}
        source = ['https://s3.amazonaws.com/dev.studionow.com/encodingcom_test/source/test_asset.mp4']
        destination = ['https://s3.amazonaws.com/dev.studionow.com/encodingcom_test/destination/test.mp4']

        self.encoding.add_media(source=source, destination=destination, format=mp4_libx264)


if __name__ == '__main__':
    from unittest import main

    main()
