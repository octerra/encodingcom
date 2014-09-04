import http.client
import urllib.parse
import json

ENCODING_API_URL = 'manage.encoding.com:80'
ENCODING_API_HEADERS = {'Content-Type':'application/x-www-form-urlencoded'}

class Encoding(object):

    def __init__(self, userid, userkey, url=ENCODING_API_URL):
        self.url = url
        self.userid = userid
        self.userkey = userkey

    def get_media_info(self, action='GetMediaInfo', ids=[], headers=ENCODING_API_HEADERS):
        fields = { 'userid':self.userid,
                   'userkey':self.userkey,
                   'action':action,
                   'mediaid':','.join(ids),
                 }

        dq = {}
        dq['query'] = fields
        query = json.dumps( dq )

        results = self._execute_request(query, headers)
        return results

    def get_status(self, action='GetStatus', ids=[], extended='no', headers=ENCODING_API_HEADERS):
        fields = { 'userid':self.userid,
                   'userkey':self.userkey,
                   'action':action,
                   'extended':extended,
                   'mediaid':','.join(ids),
                 }

        dq = {}
        dq['query'] = fields
        query = json.dumps( dq )

        results = self._execute_request(query, headers)
        return results

    def add_media(self, action='AddMedia', source=[], notify='', formats=[], instant='no', headers=ENCODING_API_HEADERS):
        fields = { 'userid':self.userid,
                   'userkey':self.userkey,
                   'action':action,
                   'source':source,
                   'notify':notify,
                   'instant':instant,
                   'format':formats
                 }

        dq = {}
        dq['query'] = fields
        query = json.dumps( dq )

        results = self._execute_request(query, headers)
        return results

    def _execute_request(self, json, headers, path='', method='POST'):
        # print('json: {0}'.format(json) )
        params = urllib.parse.urlencode({'json': json})

        conn = http.client.HTTPConnection(self.url)
        conn.request(method, path, params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        return data
