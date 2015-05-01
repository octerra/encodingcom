"""
Top level import for anyone who wants to use this package.

from encodingcom.encoding import Encoding
"""

from json import dumps, loads
from requests import post

from encodingcom.string_utils import list_to_str

from encodingcom.error_handler import ErrorHandler
from encodingcom.exception import InvalidParameterError


class Encoding(object):
    """
    Helper class to talk to Encoding.com server

    """

    ENCODING_API_URL = 'manage.encoding.com'
    API_HEADER = {'Content-Type': 'application/x-www-form-urlencoded'}

    EXIT_STATUSES = frozenset(['Finished', 'Error', 'Stopped'])

    # each state represents a given state that a mediaid can be in.
    # when querying for the status of a mediaid, one of these will be returned
    STATES = frozenset(['New', 'Downloading', 'Downloaded', 'Ready to process', 'Waitingforencoder',
                        'Processing', 'Saving', 'Finished', 'Error', 'Stopped'])

    # === default settings ===

    # encoding.com defaults to xml, we prefer json
    default_notification_format = 'json'

    # http://help.encoding.com/knowledge-base/article/what-is-instant-mode/
    # Initiate the processing to instant/immediately even though when the source media is still uploading
    default_instant = 'no'

    # === Standard Query template used in ALL core Encodingcom json data structure ===

    QUERY_TEMPLATE = {
        'query': {}
    }

    # ref: http://api.encoding.com/#VideoSettings
    # client specifying a codec without the explicit codec setting will use the default codec detailed in encoding.com

    def __init__(self, user_id: str, user_key: str,
                 notification_url: str='', error_url: str='',
                 https: bool=True):
        """
        Initializes access to package layer service

        :param user_id: str
            Encoding.com client user account id
        :param user_key: str
            Encoding.com client user account secret/key
        :param notification_url: str
            Encoding.com calls notification url when a job completion
        :param error_url: str
            Encoding.com calls notification url when a job error out
        :param https: bool
            True (default) matching encoding.com specs to use port 443 to communicate
            False otherwise using port 80
        :return: None
        """

        if https:
            self.url = 'https://' + Encoding.ENCODING_API_URL
        else:
            self.url = 'http://' + Encoding.ENCODING_API_URL

        # explicit contractual needs from the client
        self.user_id = user_id
        self.user_key = user_key

        self.notify = notification_url
        self.notify_encoding_errors = error_url

        # all other values that can be defaulted
        self._setup_defaults()

    # ===== Media APIs =====

    def add_media(self, **kwargs) -> (int, dict):
        """
        Add new media to user's queue.
        Creates new items in a queue according to formats specified in the XML API request.

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """
        if not kwargs.get('instant'):
            kwargs['instant'] = Encoding.default_instant

        # notify url is optional as encoding.com will let the target URL know when the job is done
        # if not specified, it defaults to:
        required = ['source', 'format']
        return self._request('AddMedia', required, **kwargs)

    def add_media_benchmark(self, **kwargs) -> (int, dict):
        """
        Add new media to user's queue and sets a flag to NOT process automatically after downloading
        Use this call in concert with process_media() to kick off media encoding

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """
        if not kwargs.get('instant'):
            kwargs['instant'] = Encoding.default_instant

        # notify url is optional as encoding.com will let the target URL know when the job is done
        # if not specified, it defaults to:
        required = ['source', 'format']
        return self._request('AddMediaBenchmark', required, **kwargs)

    def cancel_media(self, **kwargs):
        """
        Cancel media and its children taskid jobs

        :param kwargs:
        :return:
        """

        # TODO:  not yet validated/tested
        kwargs['mediaid'] = list_to_str(kwargs.get('mediaid', ''))

        required = ['mediaid']
        return self._request('CancelMedia', required, **kwargs)

    def get_media_info(self, extended: bool,  **kwargs) -> (int, dict):
        """
        Returns video parameters of the specified media when available.

        ref: http://api.encoding.com/#APIResponses_GetMediaInfo

        :param extended: bool
            Pass true to use the extended variant of the call
        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """

        # GetMediaInfoEx: Returns job information such as status, media file stored source storage, date, etc
        # GetMediaInfo: Returns just information about the media settings such as framerate, audio, duration, etc
        # Both calls serves different purposes...
        # GetMediaInfoEx is NOT a superset of GetMediaInfo as the return data is very different

        action = 'GetMediaInfoEx' if extended else 'GetMediaInfo'

        required = ['mediaid']
        return self._request(action, required, **kwargs)

    def get_status(self, **kwargs) -> (int, dict):
        """
        Returns information about a selected user's media and all its items in the queue.
        If mediaid in kwargs is a python list,
            it will be converted to appropriate encoding comma delimited string format

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """

        kwargs['mediaid'] = list_to_str(kwargs.get('mediaid', ''))
        if ',' in kwargs['mediaid']:
            # more than 1 specified, enable the extended flag to reflect
            kwargs['extended'] = 'yes'

        required = ['mediaid']
        return self._request('GetStatus', required, **kwargs)

    def get_media_list(self, **kwargs) -> (int, dict):
        """
        Returns a list of the user's media in the queue.
        Encoding.com returns list (encapsulated in a dict response) of all the medias it has track of.

        Note: per time of writing, encoding.com devops tells us that the mediaid span of a 2 week lifespan

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """
        required = []
        return self._request('GetMediaList', required, **kwargs)

    def process_media(self, **kwargs) -> (int, dict):
        """
        Start encoding the previously downloaded media (ones that have been added with an AddMediaBenchmark action).

        This is paired with AddMediaBenchMark as AddMediaBenchMark action does NOT start the job.
        Do not use this call with AddMedia, as an error/exception will be thrown.

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """

        # notify url is optional as encoding.com will let the target URL know when the job is done
        # if not specified, it defaults to:

        kwargs['mediaid'] = list_to_str(kwargs.get('mediaid', ''))

        required = ['mediaid', 'format']
        return self._request('ProcessMedia', required, **kwargs)

    def restart_media(self, **kwargs) -> (int, dict):
        """
        Complete restart the entire job.
        All the taskid children will also be restarted

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """
        kwargs['mediaid'] = list_to_str(kwargs.get('mediaid', ''))

        required = ['mediaid']
        return self._request('RestartMedia', required, **kwargs)

    def restart_media_errors(self, **kwargs) -> (int, dict):
        """
        Only retry tasks ended with error.

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """
        kwargs['mediaid'] = list_to_str(kwargs.get('mediaid', ''))

        required = ['mediaid']
        return self._request('RestartMediaErrors', required, **kwargs)

    def restart_media_task(self, **kwargs) -> (int, dict):
        """
        Restart specific media and taskid parts of the task

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)

        """
        # TODO: docs isn't clear or provide much details about this...
        # presumably the taskid belongs in the top level designation as the format already has been provisioned

        kwargs['mediaid'] = list_to_str(kwargs.get('mediaid', ''))

        # TODO: this is not detailed in the request template, so this is an educated guess, needs unit test to prove
        kwargs['taskid'] = list_to_str(kwargs.get('taskid', ''))

        required = ['mediaid', 'taskid']
        return self._request('RestartMediaTask', required, **kwargs)

    def stop_media(self, **kwargs) -> (int, dict):
        """
        Stop media downloading/processing/uploading.
        If at least one destination is saved, media will be finished, otherwise it will be stopped.

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """
        kwargs['mediaid'] = list_to_str(kwargs.get('mediaid', ''))

        required = ['mediaid']
        return self._request('StopMedia', required, **kwargs)

    def update_media(self, **kwargs) -> (int, dict):
        """
        ref: http://api.encoding.com/#ActionList
        Replace information about existing media's formats.
        All old format items will be deleted and the new ones will be added

        meaning:
        All the task id associated with the original job will be deleted.
        Any current job/taskid in operation WILL be stopped and cancelled

        :param kwargs:
            Variable list of arguments detailed by the client.
            Needs to match the request template (via JSON)
            ref: http://api.encoding.com/#CompleteXMLTemplate
        :return: HTTP status code, dict response from encoding.com
        :rtype: (int, dict)
        """

        # notify url is optional as encoding.com will let the target URL know when the job is done
        # if not specified, it defaults to:

        kwargs['mediaid'] = list_to_str(kwargs.get('mediaid', ''))

        required = ['mediaid', 'format']
        return self._request('UpdateMedia', required, **kwargs)

    # ===== Internal Methods =====

    def _post_request(self, json_data, header='') -> (int, dict):
        """
        Use request package and send data to the Encoding.com server.
        Process return results and handle appropriately

        :param json_data:
        :param header:
            Header for the request, defaults to standard Encoding API headers
        :return: tuple consisting of a status code from the call, and the actual content of the response.
            Encoding.com returns 200 status, but content still reflects errors
        :rtype: (string, dict)
        """
        if not header:
            header = Encoding.API_HEADER

        # all JSON data needs to be wrapped within 'json' dict in the body
        data = {'json': json_data}

        response = post(self.url, data=data, headers=header)
        status_code = response.status_code
        content = response.content.decode('utf-8')
        content = loads(content)

        return status_code, content

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

    def _request(self, action: str, requirements: [str], **kwargs) -> (int, dict):
        """
        Package and execute the request to encoding.com

        :param action:
        :param requirements: [str]
            List of required dictionary data to be found in following kwargs
        :param kwargs:
            Variable arguments from the client
        :return: tuple of HTTP status code, result response dictionary
        :rtype: (int, dict)
        """
        self._check_requirements(requirements, **kwargs)

        request = self._setup_request(action, **kwargs)
        json = dumps(request)

        status, result = self._post_request(json)
        ErrorHandler.process(result)

        return status, result

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

    from os import getenv
    from encodingcom.response_helper import get_response

    service = Encoding(getenv('ENCODING_USER_ID'), getenv('ENCODING_USER_KEY'))

    status, response = service.get_media_list()
    response = get_response(response)
    medias = response['media']
    for media in medias:
        print(media)
        print('Media Info for media: %s' % media['mediaid'])
        status, response = service.get_media_info(False, mediaid=media['mediaid'])
        response = get_response(response)
        print(response)
        print('\n')



