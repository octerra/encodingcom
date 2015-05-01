"""
String Utilities


"""

encoding_bool = lambda input_bool: 'yes' if input_bool else 'no'


def list_to_str(data, delimiter: str=',') -> str:
    """
    Convert a python list to a given string format.
    If the data is anything else but a list, original intended content is returned

    Encoding.com expects a comma delimited string output, so we have to convert data to its format.

    :param data:
        If its a list, the data is converted to a string with the comma delimited format and returned
        Everything else is simply returned back to the client
    :return: string representation using standard encoding.com delimiter: ','
    :rtype: str
    """
    if data and type(data) is list:
        # client passed in a Python list, change the format to what encoding.com expects
        return delimiter.join(data)
    else:
        # return data from client as is
        return data