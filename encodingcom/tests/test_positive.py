"""
Positive Unit test for Actions via Encoding class
"""

from logging import getLogger
from os import getenv
from unittest import TestCase

from encodingcom.encoding import Encoding
from encodingcom.exception import EncodingErrors
from encodingcom.response_helper import get_response



class EncodingPositive(TestCase):
    """
    Coverage for encoding.com positive tests
    """

    def setUp(self):
        """
        Setup a encoding.com object
        :return:
        """
        self.logger = getLogger()

        user_id = getenv('ENCODING_USER_ID')
        user_key = getenv('ENCODING_USER_KEY')
        self.encoding = Encoding(user_id, user_key)

        self.source = getenv('ENCODING_TEST_SOURCE') # Does not accept local file paths - Use http(s)://<PATH TO FILE> or FTP url

    def tearDown(self):
        pass

    def test_media_apis(self):
        """
        Positive test for medias already uploaded in encoding.com
        by using the 1st found media as a baseline for all API calls
         * get_media_list
         * get_status
         * get_media_info

        :return:
        """
        try:
            status, response = self.encoding.get_media_list()
            response = get_response(response)
            medias = response['media']
            first_media = medias[0]
            media_id = first_media.get('mediaid')
            if media_id:
                self.encoding.get_status(mediaid=media_id)
                self.encoding.get_media_info(False, mediaid=media_id)
                self.encoding.get_media_info(True, mediaid=media_id)

        except KeyError:
            # possible that there are no media currently found in the encoding.com
            pass
        except EncodingErrors:
            # Encoding Errors are possible as a job may be in a wierd state (ie. not downloaded)
            # thus resulting in an error from encoding.com
            pass
        except:
            self.fail('Unexpected exception happened, should not happen')

    def test_get_status(self):
        """
        Positive test for get_status.
        1. Single status
        2. Extended variant of the call to get multiple status(s)

        :return:
        """
        try:
            status, response = self.encoding.get_media_list()

            response = get_response(response)
            medias = response['media']

            # single media id variant
            status, result = self.encoding.get_status(mediaid=medias[0].get('mediaid'))
            self.logger.info('Multiple GetStatus (single variant) results:')
            self.logger.info(result)

            # multiple media id (extended variant of the call)
            media_ids = []
            for media in medias:
                media_ids.append(media.get('mediaid'))
            status, result = self.encoding.get_status(mediaid=media_ids)
            self.logger.info('Multiple GetStatus (extended variant) results:')
            self.logger.info(result)

        except KeyError:
            # possible that there are no media currently found in the encoding.com
            pass
        except EncodingErrors:
            # GetStatus should always function, unlike GetMediaInfo...
            # haven't found a condition where GetStatus fails with an error
            self.fail('Encoding Error happened and should not have')
        except:
            self.fail('General exception should not have happened')

    def test_add_media(self):
        """
        Positive test for get_media

        :return:
        """
        try:
            destination_format = {'output': 'mp4', 'video_codec': 'libx264'}

            status, result = self.encoding.add_media(source=self.source, format=destination_format, destination=[])

            self.logger.info('Add Media results:')
            self.logger.info(result)


        except KeyError:
            # possible that there are no media currently found in the encoding.com
            pass
        except EncodingErrors:
            # AddMedia should always function, unlike GetMediaInfo...

            self.fail('Encoding Error happened and should not have')
        except:
            self.fail('General exception should not have happened')

    def test_add_media_benchmark(self):
        """
        Positive test for get_media_benchmark.


        :return:
        """
        try:
            destination_format = {'output': 'mp4', 'video_codec': 'libx264'}

            status, result = self.encoding.add_media_benchmark(source=self.source, format=destination_format, destination=[])

            self.benchmark_result_mediaid = result['response']['MediaID']

            self.logger.info('Add Media Benchmark results:')
            self.logger.info(result)

        except KeyError:
            # possible that there are no media currently found in the encoding.com
            pass
        except EncodingErrors:
            # AddMedia should always function, unlike GetMediaInfo...

            self.fail('Encoding Error happened and should not have')
        except:
            self.fail('General exception should not have happened')


    def test_process_media(self):
        """
        Positive test for process_media


        :return:
        """

        status, response = self.encoding.get_media_list()
        response = get_response(response)
        media = response['media']

        media_id = None

        for item in media:

            file_url = item['mediafile']

            filename = self.get_filename_from_url(file_url)
            test_filename = self.get_filename_from_url(self.source)

            if filename == test_filename and 'Ready to process' in item['mediastatus']:
                media_id = item['mediaid']
                break

        if media_id:

            try:
                status, result = self.encoding.process_media(mediaid=media_id, format={'output': 'mp4', 'video_codec': 'libx264'})

                if not result['response']['message'] == 'Started':
                    self.fail('Media was not started')

            except KeyError:
                self.fail('Did not return expected response')



    def test_get_media_list(self):
        """
        Positive test for get_media_list


        :return:
        """

        status, result = self.encoding.get_media_list()


    def get_filename_from_url(self, file_url):

        file_url_components = file_url.split('/')
        filename = file_url_components[len(file_url_components)-1]

        return filename

if __name__ == '__main__':
    from unittest import main

    main()
