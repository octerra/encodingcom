"""
Provide a set of util functions to fetch data out from a given response dict.

"""


def get_response(data: dict) -> dict:
    """
    Retrieve encoding.com standard "response" dict from the given data.

    :param data:
    :return: Dictionary representing the response, {} if not found
    :rtype: dict
    """
    response = data.get('response')
    if response:
        return response
    else:
        return {}


def get_media_id(data: dict) -> str:
    """
    Retrieve encoding.com standard "mediaid" dict from the given data.

    :param data: response dictionary from a call to encoding.com
    :return: media_id matching the "MediaID" from a call to encoding.com, '' if not found
    :rtype: dict
    """
    response = get_response(data)
    return response.get('MediaID', '')