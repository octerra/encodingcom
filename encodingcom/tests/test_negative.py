"""
Unit test for all properties
Positive and Negative tests
"""

from unittest import TestCase

from encodingcom.encoding import Encoding
from encodingcom.exception import EncodingErrors


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
        self.encoding = Encoding('user_id', 'user_key')

    def tearDown(self):
        pass

    def test_get_media_info(self):
        """
        Negative test for GetMediaInfo:
        * Missing media id from client
        * Invalid media id not found

        :return:
        """
        with self.assertRaises(EncodingErrors):
            self.encoding.get_media_info(mediaid=[])
            self.encoding.get_media_info(mediaid=['1', '2'])

    def test_get_status(self):
        """
        Negative test for GetStatus:
        * invalid mediaid using both python list and native encoding.com expected

        :return:
        """
        with self.assertRaises(EncodingErrors):
            self.encoding.get_status(mediaid=['1', '2'])
            self.encoding.get_status(mediaid='1, 2')

    def test_add_media(self):
        """

        :return:
        """
        mp4_libx264 = {'output': 'mp4', 'video_codec': 'libx264'}

        with self.assertRaises(EncodingErrors):
            self.encoding.add_media(source=[], format=mp4_libx264)


if __name__ == '__main__':
    from unittest import main

    main()
