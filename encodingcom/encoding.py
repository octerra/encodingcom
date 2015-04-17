"""

"""

from http.client import HTTPConnection
from urllib.parse import urlencode
from json import dumps

from exceptions import InvalidParameterError, InvalidIdentity
from format import Format

class Encoding(object):
    """
    Helper class to talk to Encoding.com server

    """

    ENCODING_API_URL = 'manage.encoding.com'
    API_HEADER = {'Content-Type': 'application/x-www-form-urlencoded'}

    # === default settings ===

    # encoding.com defaults to xml, we prefer json
    default_notification_format = 'json'

    # http://help.encoding.com/knowledge-base/article/what-is-instant-mode/
    # Initiate the processing to instant/immediately even though when the source media is still uploading
    default_instant = 'no'

    # === Standard Query template ===

    QUERY_TEMPLATE = {
        'query': {}
    }

    # adhere to: http://api.encoding.com/#ActionList
    ACTIONS = {
        'AddMedia': '',
        'AddMediaBenchmark': '',
        'UpdateMedia': '',
        'ProcessMedia': '',
        'CancelMedia': '',
        'GetMediaList': '',
        'GetStatus': '',
        'GetMediaInfo': '',
        'GetMediaInfoEx': '',
        'RestartMedia': '',
        'RestartMediaErrors': '',
        'RestartMediaTask': '',
        'StopMedia': ''
    }

    # ref: http://api.encoding.com/#VideoSettings
    # client specifying a codec without the explicit codec setting will use the default codec detailed in encoding.com


    def __init__(self, user_id: str, user_key: str,
                 notification_url: str='', error_url: str='',
                 https: bool=True):
        """

        :param user_id: str
        :param user_key: str
        :param notification_url: str
        :param error_url: str

        :param https: bool
            True (default) matching encoding.com specs to use port 443 to communicate
            False otherwise using port 80
        :return: None
        """

        if https:
            self.url = Encoding.ENCODING_API_URL + ':443'
        else:
            self.url = Encoding.ENCODING_API_URL + ':80'

        # explicit contractual needs from the client
        self.user_id = user_id
        self.user_key = user_key

        self.notify = notification_url
        self.notify_encoding_errors = error_url

        # all other values that can be defaulted
        self.setup_defaults()

    def setup_defaults(self):
        """
        Setup instance object to reflect client settings
        Only specify default settings that falls in this criteria:
         * override the default natural Encoding.com defaults
         * hidden or non documented settings

        client can override these settings with explicit property setters after construction of object

        :return: None
        """
        self.notification_format = Encoding.default_notification_format
        self.instant = Encoding.default_instant

    def setup_core_request(self, action: str) -> dict:
        """
        Setup the core request body specifics

        :param action: str
            Action to be performed

        :return: dictionary with the core request required components
        :rtype: dict
        """

        query = Encoding.QUERY_TEMPLATE.copy()
        body = {'userid': self.user_id,
                'userkey': self.user_key,
                'action': action}
        query['query'] = body
        return query

    def setup_request(self, action: str, **kwargs):
        """
        Generic setup request for delivery to encoding.com

        :param action: str
            action desired
        :param kwargs: dict
            Arguments provided by the client
        :return:
            dict representing the built request
        :rtype: dict
        """

        request = self.setup_core_request(action)

        query_dict = request['query']
        for key in kwargs:
            query_dict[key] = kwargs[key]

        return request

    # def get_media_info(self, ids=None, headers=''):
    def get_media_info(self, **kwargs):
        """

        ref: http://api.encoding.com/#APIResponses_GetMediaInfo

        :param ids:
        :return:
        """

        request = self.setup_request('GetMediaInfo', **kwargs)
        json = dumps(request)

        results = self._execute_request(json, Encoding.API_HEADER)

        # TODO: process and handle results for errors, and map them to appropriate response for clients

        return results

    def get_status(self, ids=None, extended='no', headers=API_HEADER):
        """

        :param ids:
        :param extended:
        :param headers:
        :return:
        """
        if not ids:
            ids = []

        fields = {'userid': self.user_id,
                  'userkey': self.user_key,
                  'action': 'GetStatus',
                  'extended': extended,
                  'mediaid': ','.join(ids)}

        dq = dict()
        dq['query'] = fields
        query = dumps(dq)

        results = self._execute_request(query, headers)
        return results

    # def add_media(self, source=None, notify='', notify_format='', formats=None,
    #               instant='no', headers=ENCODING_API_HEADERS):

    def add_media(self, **kwargs):
        """


        :return:
        """
        request = self.setup_request('AddMedia', **kwargs)
        json = dumps(request)

        results = self._execute_request(json, headers=Encoding.API_HEADER)
        return results

    # TODO: use Requests and move this elsewhere
    def _execute_request(self, json_data, headers, path='', method='POST'):
        """

        :param json_data:
        :param headers:
        :param path:
        :param method:
        :return:
        """
        # print('json: {0}'.format(json) )
        params = urlencode({'json': json_data})

        conn = HTTPConnection(self.url)
        conn.request(method, path, params, headers)
        response = conn.getresponse()
        # TODO: Better handling of response, ie. errors
        data = response.read()
        conn.close()

        return data


if __name__ == '__main__':
    service = Encoding('id', 'key')

    # service.add_media(source='http://snwatsonclientuploads.s3.amazonaws.com/gj6244b1ngq7o9-1.mp4')

    service.get_media_info(mediaid=['1', '2'])
