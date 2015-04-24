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
        self.encoding = Encoding('user_id', 'user_key')

    def tearDown(self):
        pass

    def test_add_media(self):
        """
        Test add media call
        :return:
        """
        pass

    def test_media_apis(self):
        """
        Positive test for medias already uploaded in encoding.com:
         * get_media_list
         * get_status
         * get_media_info

        :return:
        """
        status, result = self.encoding.get_media_list()
        try:
            medias = result['response']['media']
            first_media = medias[0]
            media_id = first_media.get('mediaid')
            if media_id:
                status, result = self.encoding.get_status(mediaid=media_id)
                status, result = self.encoding.get_media_info(mediaid=media_id)

        except KeyError:
            # possible that there are no media currently found in the encoding.com
            pass
        except EncodingErrors:
            self.fail('Encoding Error happened and should not have')

if __name__ == '__main__':
    from unittest import main

    main()
