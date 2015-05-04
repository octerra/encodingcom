"""
Polls Encoding.com for a specific mediaid until an exit condition is hit

Encoding.com notification only calls a URL upon success/failure condition.
Tool allows clients to keep track of the state change for a given mediaid.

Written for educational and testing purposes only.
Pollers are obviously spammy and should only be used where appropriate.

"""

from os import getenv
from time import sleep

from encodingcom.encoding import Encoding
from encodingcom.response_helper import get_response
from encodingcom.encoding_utils import get_latest_media


class Poller(object):
    """

    """

    @staticmethod
    def poll_till_status(service: Encoding, media_id: str, callback=None, status='Finished', interval: float=5):
        """
        Continuously update the status of the given media_id until desired state.
        Call the given callback to handle the completion state

        Note: Written to support a non-notification url workflow only.
            We should support notification URL as this will generate a lot of noise.
            Any sleep states to encoding.com may miss states that complete very fast and will NOT be caught by polling.
            "finished" or "error" state is one that is always reflects completion

        :param service: Encoding
            service class to Encoding
        :param media_id: str
            Desired media_id to poll status for
        :param callback:
            Client callback to invoke once encountering desired status (optional)
            If no callback specified, this will poll until desired status or until exit condition is satisfied

            Error and Finished status also triggers this call as this marks the end of the job and
                status not encountered during polling
        :param status: str
            desired state for callback.
            Should the status not be found, callback will be invoked for either "finished" or "error"
        :param interval: float
            Interval between each polling operation

        :return: last state reflected by GetStatus action
        :rtype: dict
        """

        if status not in Encoding.EXIT_STATUSES:
            exit_statuses = set(Encoding.EXIT_STATUSES)
            exit_statuses.add(status)
        else:
            exit_statuses = Encoding.EXIT_STATUSES

        while True:
            http_status, response = service.get_status(mediaid=media_id)
            response = get_response(response)
            status = response['status']

            if status in exit_statuses:
                if callback:
                    callback(media_id=media_id, status=status, response=response)
                return response

            sleep(interval)

    @staticmethod
    def poll_status(service: Encoding, media_id: str, callback=None, status='Finished', interval: float=5):
        """
        Continuously poll for status changes from the prior state.

        :param service: Encoding
            service class to Encoding
        :param media_id: str
            Desired media_id to poll status for
        :param callback:
            Client callback to invoke per state change encountered
            If no callback specified, this will poll until desired status or until exit condition is satisfied

            Error and Finished status also triggers this call as this marks the end of the job and
                status not encountered during polling
        :param status:
        :param interval: float
            Interval to poll at... some of these states goes by very quickly depending on the encoding.com bandwidth
            Set to spammy 0 if you want to track all the changes
        :return: None
        """

        if status not in Encoding.EXIT_STATUSES:
            exit_statuses = set(Encoding.EXIT_STATUSES)
            exit_statuses.add(status)
        else:
            exit_statuses = Encoding.EXIT_STATUSES

        last_status = ''
        while True:
            http_status, response = service.get_status(mediaid=media_id)
            response = get_response(response)
            status = response['status']

            if status != last_status:
                last_status = status
                if callback:
                    callback(media_id=media_id, status=status, response=response)

            if status in exit_statuses:
                return response

            sleep(interval)

    @staticmethod
    def print_response(**kwargs):
        """
        Simply print the response from encoding.com

        :param
        :return: None
        """
        print('MediaID {0} response for status {1}:\n{2}'.format(
            kwargs['media_id'], kwargs['status'], str(kwargs['response'])))


if __name__ == '__main__':

    encoding = Encoding(getenv('ENCODING_USER_ID'), getenv('ENCODING_USER_KEY'))
    media = get_latest_media(encoding)

    # track each state polling
    Poller.poll_status(encoding, media_id=media['mediaid'], callback=Poller.print_response, interval=0)


    # poll till status variant
    Poller.poll_till_status(encoding, media_id=media['mediaid'], callback=Poller.print_response)
    # response = Poller.poll_till_status(encoding, media_id=media['mediaid'])
