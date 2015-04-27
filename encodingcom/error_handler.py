"""
Error handler for Encoding.com

Checks and process errors.
Maps errors into exceptions for clients to catch

"""

from encodingcom.exception import EncodingErrors

class ErrorHandler(object):
    """
    Error Handler for Encoding.com
    """

    @staticmethod
    def get_errors(response: dict) -> [str]:
        """
        Check and retrieve for existence of any errors from the response dictionary
        If an error is found, return the error(s) as a list, as 1 or more errors can be returned

        Checking for the HTTP status code is insufficient as this simply reflects delivery success/failure.
        Details of the response are buried within

        Response structure:
            (HTTP status code, details_dict)
            details_dict = {
                'response': dict {
                    'errors': {
                        'error': 'specific error information
                    }
                'other data': dict {
                }
            }

        :return: list of errors found
        :rtype: list
        """
        result = []

        try:
            # all the details are encapsulated in a dict
            for key in response.keys():
                if 'errors' in response[key]:
                    errors = response[key]['errors']
                    for error_key in errors.keys():
                        # there can be > 1 error from encoding.com
                        result.append(errors[error_key])
                    return result
                else:
                    # other data can also be found in the response
                    pass
        except KeyError:
            # Errors needs to follow a specific documented return specifics
            # Processing of the error has changed, likely encoding.com contract changes
            assert False

        return result

    @staticmethod
    def process(response: dict):
        """
        Process any errors detailed in the response.
        Errors found raise an exception with a list of errors

        :param response: dict
            Response dictionary from encoding.com
        :return: None
        """
        errors = ErrorHandler.get_errors(response)
        if not errors:
            return

        raise EncodingErrors(errors)

