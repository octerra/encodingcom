"""

"""

from http.client import HTTPConnection
from urllib.parse import urlencode
from json import dumps

from exceptions import InvalidParameterError, InvalidIdentity


class Encoding(object):
    """
    Helper class to talk to Encoding.com server

    """

    ENCODING_API_URL = 'manage.encoding.com'
    ENCODING_API_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

    VALID_REGIONS = ['us-east-1', 'us-west-1', 'us-west-2', 'eu-west-1',
                     'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'sa-east-1']

    VALID_FORMATS = ['xml','json']

    # === default settings ===
    # encoding.com default processing is us-east-1 if not specified, we choose Northern California for default
    # override to use one that is suitable to your needs
    default_region = 'us-west-1'

    default_notification_format = 'json'


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

    # adhere to: http://api.encoding.com/#SourceMediaLocation
    SOURCE_MEDIA_LOCATION = {
        'HTTP': '',
        'FTP': '',
        'SFTP': '',
        'S3': '',
        'Rackspace CloudFiles': '',
        'Aspera Server': '',
        'Windows Azure Blob': '',
        'OpenStack Cloud Storage': ''
    }

    # ref: http://api.encoding.com/#VideoSettings
    # client specifying a codec without the explicit codec setting will use the default codec detailed in encoding.com
    VIDEO_CODEC = {
        'flv': {'flv': '', 'libx264': '', 'vp6': ''},
        'fl9': {'libx264': ''},
        'wmv': {'wmv2': '', 'msmpeg4': ''},
        'zune': {'wmv2': '', 'msmpeg4': ''},
        '3gp': {'h263': '', 'mpeg4': '', 'libx264': ''},
        'android': {'h263': '', 'mpeg4': '', 'libx264': ''},
        'm4v': {'mpeg4': ''},
        'ipod': {'mpeg4': '', 'libx264': ''},
        'iphone': {'mpeg4': '', 'libx264': ''},
        'appletv': {'mpeg4': '', 'libx264': ''},
        'psp': {'mpeg4': '', 'libx264': ''},
        'mp4': {'mpeg4': '', 'libx264': '', 'hevc': ''},
        'ogg': {'libtheora': ''},
        'webm': {'libvpx': ''},
        'mp3': {},
        'wma': {},
        'mpeg2': {'mpeg2video': ''},
        'mpeg1': {'mpeg1video': ''},
        'mov': {'mpeg4': '', 'libx264': '', 'xdcam': '', 'dvcpro': '', 'dvcpro50': '', 'dvcprohd': '', 'mjpeg': ''},
        'mpegts': {'libx264': '', 'mpeg2video': ''},
        'mxf': {'dvcpro': '', 'dvcpro50': '', 'dvcprohd': '', 'xdcamhd422': ''}
    }


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

    def get_media_info(self, ids=None, headers=''):
        """

        :param ids:
        :param headers:
        :return:
        """
        if not ids:
            ids = []
        if not headers:
            headers = Encoding.ENCODING_API_HEADERS

        fields = {'userid': self.user_id,
                  'userkey': self.user_key,
                  'action': 'GetMediaInfo',
                  'mediaid': ','.join(ids)}

        dq = dict()
        dq['query'] = fields
        query = dumps(dq)

        results = self._execute_request(query, headers)
        return results

    def get_status(self, ids=None, extended='no', headers=ENCODING_API_HEADERS):
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

    def add_media(self, source=None, notify='', notify_format='', formats=None,
                  instant='no', headers=ENCODING_API_HEADERS):
        """

        :param source:
        :param notify:
        :param notify_format:
        :param formats:
        :param instant:
        :param headers:
        :return:
        """
        if not source:
            source = []
        if not formats:
            formats = []

        fields = {'userid': self.user_id,
                  'userkey': self.user_key,
                  'action': 'AddMedia',
                  'source': source,
                  'notify': notify,
                  'notify_format': notify_format,
                  'instant': instant,
                  'format': formats}

        dq = dict()
        dq['query'] = fields
        query = dumps(dq)

        results = self._execute_request(query, headers)
        return results

    # === Property Settings ===
    # property naming constructs strictly adhere to Encoding.com JSON template definitions

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if value:
            self._user_id = value
        else:
            raise InvalidIdentity(value)

    @property
    def user_key(self):
        return self._user_key

    @user_key.setter
    def user_key(self, value):
        if value:
            self._user_key = value
        else:
            raise InvalidIdentity(value)

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        # everything has defaults, use iff valid
        if value in Encoding.VALID_REGIONS:
            self._region = value

    @property
    def notification_format(self):
        return self._notification_format

    @notification_format.setter
    def notification_format(self, value):
        # everything has defaults, use iff valid
        if value in Encoding.VALID_FORMATS:
            self._notification_format = value

    @property
    def notify(self):
        return self._notify

    @notify.setter
    def notify(self, value):
        # TODO: ensure that this is urlencode
        self._notify = value

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
    def video_codec(self):
        return self._video_codec

    @video_codec.setter
    def video_codec(self, value: str):
        """
        :param value: str
            Video codec setting is a string comprised of a valid "codec type:encoder"
            For example:
            "mov:libx264" specifies an exact video codec and libx264 encoder used for mov format.
            "mov" without a explicit encoder specification results in using the default format used for "mov".
                In this case, the default is "mpeg4"

        :return: None
        """
        parts = value.split(':')
        if 1 == len(parts):
            # use the default format
            if value not in Encoding.VIDEO_CODEC:
                raise InvalidParameterError(value)
        elif 2 == len(parts):
            encoder_type = parts[0]
            encoder = parts[1]
            try:
                result = Encoding.VIDEO_CODEC[encoder_type][encoder]
            except KeyError:
                raise InvalidParameterError(value)
        else:
            raise InvalidParameterError('Incorrect video codec parameter designation')


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
    service = Encoding('my_id', 'my_key')
