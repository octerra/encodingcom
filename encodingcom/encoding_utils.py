"""
Set of utility methods to help clients to access data

"""

from encodingcom.encoding import Encoding
from encodingcom.response_helper import get_response


def get_latest_media(service: Encoding) -> dict:
    """
    Get latest media id information

    :param service: Encoding
        Encoding service class
    :return: dictionary response from the encoding.com
    :rtype: dict
    """
    status, response = service.get_media_list()
    response = get_response(response)
    medias = response['media']
    return medias[len(medias) - 1]


def get_oldest_media(service: Encoding) -> dict:
    """
    Get latest media id information

    :param service: Encoding
        Encoding service class
    :return: dictionary response from the encoding.com
    :rtype: dict
    """
    status, response = service.get_media_list()
    response = get_response(response)
    medias = response['media']
    return medias[0]

