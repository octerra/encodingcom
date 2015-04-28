"""
Provide set of unit tests for format specifics

"""


from logging import getLogger
from unittest import TestCase

from encodingcom.format import Format
from encodingcom.exception import EncodingErrors


class FormatTests(TestCase):
    """
    Coverage for encoding.com positive tests
    """

    def setUp(self):
        """
        Setup a encoding.com object
        :return:
        """
        self.logger = getLogger()

    def tearDown(self):
        pass

    def test_thumbnail_format(self):
        """
        Test all the various thumbnail formats possible

        :return:
        """

        required = ['output', 'file_extension', 'keep_aspect_ratio']
        thumbnail = Format.thumbnail()
        for item in required:
            if item not in thumbnail:
                self.fail('Expected key in the thumbnail not found: %s' % item)


if __name__ == '__main__':
    from unittest import main

    main()
