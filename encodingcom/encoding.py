"""
Encoding-py3 service package.

Features:

Core Functionality:
* Wrap and deliver encoding.com with ease
* Handle processing of error returns, map to appropriate serviceable python exceptions
    Many encoding.com 2xx returns are reflection of a successful call, but in actual the call has failed.
    Handle these contextual error scenarios so client can handle more appropriately
* Uses JSON for core delivery and response content, much nicer than XML encoding.com defaults

Additional Features:
* Tracking multiple task IDs (different encoding tasks for the same media ID)
* Enable clients to reuse the same media id for processing.
    ref:  UpdateMedia, ProcessMedia, CancelMedia, GetMediaInfo, GetStatus.

Design Principles:
* No contract enforcements in Encoding.com Request Template, use Encoding.com defaults to be used.
    If settings are missing from the contents, defaults will be used.
    Meaning the client has to be aware of the defaults, as default settings will having varying outcomes.

* Basic key guards put into Encoding.com Request Template
    Minimize number of errors by provision key needed request template needs.
    Items such as keys, secret, response format, etc are automatically provisioned

*



"""

from json import dumps, loads
from requests import post
from requests.models import Response
from requests.exceptions import HTTPError

from encodingcom.error_handler import ErrorHandler
from encodingcom.exception import InvalidParameterError, InvalidIdentity

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
            self.url = 'https://' + Encoding.ENCODING_API_URL
            # self.url = Encoding.ENCODING_API_URL + ':443'
        else:
            self.url = 'http://' + Encoding.ENCODING_API_URL
            # self.url = Encoding.ENCODING_API_URL + ':80'

        # explicit contractual needs from the client
        self.user_id = user_id
        self.user_key = user_key

        self.notify = notification_url
        self.notify_encoding_errors = error_url

        # all other values that can be defaulted
        self._setup_defaults()

    # def get_media_info(self, ids=None, headers=''):
    def get_media_info(self, **kwargs):
        """

        ref: http://api.encoding.com/#APIResponses_GetMediaInfo

        :param ids:
        :return:
        """

        required = ['mediaid']
        return self._request('GetMediaInfo', required, **kwargs)

    def get_status(self, **kwargs):
        """
        Returns information about a selected user's media and all its items in the queue.
        If mediaid in kwargs is a python list,
            it will be converted to appropriate encoding comma delimited string format

        :return:
        """

        mediaid = kwargs.get('mediaid')
        if mediaid and type(mediaid) is list:
            # client passed in a Python list, change the format to what encoding.com expects
            kwargs['extended'] = True
            kwargs['mediaid'] = ','.join(kwargs['mediaid'])
        else:
            # take the input from client as is
            pass

        required = ['mediaid']
        return self._request('GetStatus', required, **kwargs)

    # def add_media(self, source=None, notify='', notify_format='', formats=None,
    #               instant='no', headers=ENCODING_API_HEADERS):
    def add_media(self, **kwargs):
        """
        Add new media to user's queue.
        Creates new items in a queue according to formats specified in the XML API request.

        :return:
        """
        if not kwargs.get('instant'):
            kwargs['notify_format'] = Encoding.default_instant

        # notify url is optional as encoding.com will let the target URL know when the job is done
        # if not specified, it defaults to:
        required = ['source', 'format']
        return self._request('GetStatus', required, **kwargs)

    # ===== Internal Methods =====

    def _post_request(self, json_data, header=None) -> (int, str):
        """
        Use request package and send data to the Encoding.com server.
        Process return results and handle appropriately

        :param json_data:
        :param header:
            Header for the request, defaults to standard Encoding API headers
        :return: tuple consisting of a status code from the call, and the actual content of the response.
            Encoding.com returns 200 status, but content still reflects errors
        :rtype: (string, string)
        """
        if not header:
            header = Encoding.API_HEADER

        try:
            # all JSON data needs to be wrapped within 'json' dict in the body
            data = {'json': json_data}

            response = post(self.url, data=data, headers=header)
            status_code = response.status_code
            content = response.content.decode('utf-8')
            content = loads(content)

            return status_code, content
        except HTTPError as ex:
            status_code = ex.response.status_code
            response = ex.response
            # TODO: Better handling

    def _setup_core_request(self, action: str) -> dict:
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
                'notify_format': Encoding.default_notification_format,
                'action': action}
        query['query'] = body
        return query

    def _setup_request(self, action: str, **kwargs) -> dict:
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

        request = self._setup_core_request(action)

        query_dict = request['query']
        for key in kwargs:
            query_dict[key] = kwargs[key]

        return request

    def _request(self, action: str, requirements: [str], **kwargs):
        """
        Package and execute the request to encoding.com

        :param action:
        :param requirements: [str]
            List of required dictionary data to be found in following kwargs
        :param kwargs:
            Variable arguments from the client
        :return:
        """
        self._check_requirements(requirements, **kwargs)

        request = self._setup_request(action, **kwargs)
        json = dumps(request)

        # results = self._execute_request(json, Encoding.API_HEADER)
        result = self._post_request(json)
        ErrorHandler.process(result)

        return result

    def _setup_defaults(self):
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

    @staticmethod
    def _check_requirements(required_params: list, **kwargs) -> bool:
        """
        Ensure that all the required parameters are found.
        Throws an exception if not found to tell the caller the call is malformed.

        :param **kwargs:
            Client API invocation arguments
        :param required_params: list

        :return: True if all the params has been found
        :rtype: bool
        """
        for param in required_params:
            if param not in kwargs:
                raise InvalidParameterError('Missing parameter: %s' % param)
        return True



if __name__ == '__main__':
    # TODO: remove keys before going into Pypi
    service = Encoding('33524', '151ff24e4fcf5f18b33468d129bd36c7')

    mp4_libx264 = {'output': 'mp4', 'video_codec': 'libx264'}
    service.add_media(source=[], format=mp4_libx264)

    # service.add_media(source='http://snwatsonclientuploads.s3.amazonaws.com/gj6244b1ngq7o9-1.mp4')

    # destination_format = {'output': format_specs['output']}
