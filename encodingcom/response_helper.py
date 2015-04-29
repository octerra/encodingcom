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

    :param data: dict
        Entire response data returned by any of the calls to encoding.com
    :return: media_id matching the "MediaID" from a call to encoding.com, '' if not found
    :rtype: str
    """
    response = get_response(data)
    if response:
        return response.get('MediaID', '')
    else:
        return {}


def get_format(data: dict) -> dict:
    """
    Retrieve the format section in the response.

    :param data: dict
        Entire response data returned by any of the calls to encoding.com
    :return:
        dictionary representing all the format contents of the response
        If there is no format in response found, empty dict is returned
    :rtype: dict
    """
    response = get_response(data)
    if response:
        result = response.get('format')
        if result:
            return result

    return {}