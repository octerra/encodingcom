import http.client
import urllib.parse
import json

ENCODING_API_URL = 'manage.encoding.com:80'
ENCODING_API_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}


class Encoding(object):
    """
    Helper class to talk to Encoding.com server

    """

    def __init__(self, user_id, user_key, url=ENCODING_API_URL):
        self.url = url
        self.user_id = user_id
        self.user_key = user_key

    def get_media_info(self, action='GetMediaInfo', ids=None, headers=ENCODING_API_HEADERS):
        """

        :param action:
        :param ids:
        :param headers:
        :return:
        """
        if not ids:
            ids = []

        fields = {'userid': self.user_id,
                  'userkey': self.user_key,
                  'action': action,
                  'mediaid': ','.join(ids)}

        dq = dict()
        dq['query'] = fields
        query = json.dumps(dq)

        results = self._execute_request(query, headers)
        return results

    def get_status(self, action='GetStatus', ids=None, extended='no', headers=ENCODING_API_HEADERS):
        """

        :param action:
        :param ids:
        :param extended:
        :param headers:
        :return:
        """
        if not ids:
            ids = []

        fields = {'userid': self.user_id,
                  'userkey': self.user_key,
                  'action': action,
                  'extended': extended,
                  'mediaid': ','.join(ids)}

        dq = dict()
        dq['query'] = fields
        query = json.dumps(dq)

        results = self._execute_request(query, headers)
        return results

    def add_media(self, action='AddMedia', source=None, notify='', notify_format='', formats=None,
                  instant='no', headers=ENCODING_API_HEADERS):
        """

        :param action:
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
                  'action': action,
                  'source': source,
                  'notify': notify,
                  'notify_format': notify_format,
                  'instant': instant,
                  'format': formats}

        dq = dict()
        dq['query'] = fields
        query = json.dumps(dq)

        results = self._execute_request(query, headers)
        return results

    def _execute_request(self, json, headers, path='', method='POST'):
        """

        :param json:
        :param headers:
        :param path:
        :param method:
        :return:
        """
        # print('json: {0}'.format(json) )
        params = urllib.parse.urlencode({'json': json})

        conn = http.client.HTTPConnection(self.url)
        conn.request(method, path, params, headers)
        response = conn.getresponse()
        # TODO: Better handling of response, ie. errors
        data = response.read()
        conn.close()

        return data
