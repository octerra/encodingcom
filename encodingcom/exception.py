"""
Exceptions to support encoding.com

"""


class EncodingExceptionBase(Exception):
    """
    Base class for handle encoding.com exceptions
    """

    def __init__(self, message: str, data: str=''):
        self.message = ''.join([message, '\nData:\n', data])

    def __str__(self):
        return self.message


class InvalidIdentity(EncodingExceptionBase):
    """
    Invalid client identity or key given
    """
    def __init__(self, user_id: str, user_key):
        error = 'Invalid client identity %s or key %s designated' % (user_id, user_key)
        super().__init__(error)


class InvalidParameterError(EncodingExceptionBase):
    """
    Given designation is invalid in either parameter or settings.
    Does not match encoding.com allows
    """
    def __init__(self, param: str):
        error = 'Specified parameter given is invalid: {0}'.format(param)
        super().__init__(error)


class EncodingErrors(EncodingExceptionBase):
    """
    Given designation is invalid in either parameter or settings.
    Does not match encoding.com allows
    """
    def __init__(self, error):
        """

        :param error:
            Error can be either a string or a list of errors
        :return:
        """

        error = 'Encoding.com error response {0}'.format(error)
        super().__init__(error)


