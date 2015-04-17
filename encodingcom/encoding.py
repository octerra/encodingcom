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
    # encoding.com default processing is us-east-1 if not specified, we choose Northern California for default
    # override to use one that is suitable to your needs
    default_region = 'us-west-1'

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
        setup instance object with the defaults used in the system.
        client can override these settings with explicit property setters after construction of object

        :return:
        """
        self.region = Encoding.default_region
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

    def setup_request(self, action: str, required_keys: list, **kwargs):
        """
        Generic setup request for delivery to encoding.com

        :param action: str
            action desired
        :param required_keys: list
            List of required keys.  Ensures that all the keys has been defined by the client
        :param kwargs: dict
            Arguments provided by the client
        :return:
            dict representing the built request
        :rtype: dict
        """

        request = self.setup_core_request(action)

        for key in required_keys:
            value = kwargs.get(key)
            if value:
                self.__setattr__(key, kwargs[key])
                request['query'][key] = getattr(self, key)
            else:
                raise InvalidParameterError(key)

    # def get_media_info(self, ids=None, headers=''):
    def get_media_info(self, **kwargs):
        """

        ref: http://api.encoding.com/#APIResponses_GetMediaInfo

        :param ids:
        :return:
        """

        required_keys = ['mediaid']

        request = self.setup_request('GetMediaInfo', required_keys, **kwargs)
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
        required_keys = ['source', 'notify', 'notify_format', 'format']

        request = self.setup_request('AddMedia', required_keys, **kwargs)

        results = self._execute_request(request, headers=Encoding.API_HEADER)
        return results

    # === Property Settings ===
    # property naming constructs strictly adhere to Encoding.com JSON template definitions

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        if value:
            self._user_id = value
        else:
            raise InvalidIdentity('user_id')

    @property
    def user_key(self):
        return self._user_key

    @user_key.setter
    def user_key(self, value: str):
        if value:
            self._user_key = value
        else:
            raise InvalidIdentity('user_key')

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value: str):
        """
        ref: http://api.encoding.com/#Global Processing Regions

        :param value: str
            desired region for processing
        :return:
        """

        valid_regions = {
            'us-east-1': '', 'us-west-1': '', 'us-west-2': '', 'eu-west-1': '',
            'ap-southeast-1': '', 'ap-southeast-2': '', 'ap-northeast-1': '', 'sa-east-1': ''}

        if value in valid_regions:
            self._region = value
        else:
            raise InvalidParameterError('region')

    @property
    def instant(self):
        return self._instant

    @instant.setter
    def instant(self, value: str):
        """
        Set the prcessing mode to instant.

        :param value: str
        :return:
        """
        # TODO: dont know if these valus are correct as there is no template definition or API spec documented
        valid_instant = ['yes', 'no']
        if value in valid_instant:
            self._instant = value
        else:
            raise InvalidParameterError('instant')

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value: str):
        """
        Source must adhere to one of the specified acceptable URI designation (ie. http/sftp/...)

        ref: http://api.encoding.com/#SourceMediaLocation

        :param value:
        :return:
        """
        valid_source = {
            'http': '', 'https': '', 'ftp': '', 'sftp': '', 'fasp': '', 'swift': ''
        }

        uri = value.lower()
        index = uri.find('://')
        if -1 == index:
            raise InvalidParameterError('source does not have a proper protocol designation')
        else:
            protocol = uri[0:index]
            if protocol in valid_source:
                self._source = uri
            else:
                raise InvalidParameterError('Invalid protocol found: %s' % protocol)

    @property
    def mediaid(self):
        return self._mediaid

    @mediaid.setter
    def mediaid(self, value: list):
        """
        List of media ids

        :param value: list
            python list of media IDs
        :return:
        """
        self._mediaid = '.'.join(value)

    @property
    def notify_format(self):
        return self._notification_format

    @notify_format.setter
    def notify_format(self, value):
        """
        Notification format

        :param value:
        :return:
        """
        valid_notify_format = ['xml','json']

        if value in valid_notify_format:
            self.notify_format = value
        else:
            raise InvalidParameterError('notify_format')

    @property
    def notify(self):
        return self._notify

    @notify.setter
    def notify(self, value):
        valid_notify = {
            'http': '', 'https': '', 'mailto': ''
        }
        if value in valid_notify:
            self._notify = value
        else:
            raise InvalidParameterError('notify')

    @property
    def notify_encoding_errors(self):
        return self._notify_encoding_errors

    @notify_encoding_errors.setter
    def notify_encoding_errors(self, value):
        # TODO: ensure that this is urlencode
        self._notify_encoding_errors = value

    @property
    def notify_upload(self):
        return self._notify_upload

    @notify_upload.setter
    def notify_upload(self, value):
        # TODO: ensure that this is urlencode
        self._notify_upload = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if isinstance(value, Format):
            self._format = value
        else:
            raise InvalidParameterError('format')

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
    service = Encoding('33524', '151ff24e4fcf5f18b33468d129bd36c7')

    service.source = 'http://snwatsonclientuploads.s3.amazonaws.com/gj6244b1ngq7o9-1.mp4'
    service.add_media()

    # service.get_media_info(mediaid=['1', '2'])
