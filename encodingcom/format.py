
"""
Provide format data constructors to adhere to encoding.com needs

"""


class Format(object):
    """
    Provide format data constructors to adhere to encoding.com needs

    """

    @staticmethod
    def thumbnail(time: str='', video_codec: str='', width: str='', keep_aspect_ratio: bool=True,
                  rotate: str='', file_extension: str='jpg'):
        """
        Helper method to build a thumbnail format using the given values.
        thumbnail is not well documented in the encoding.com API specs,
        following reflect contract given from devops representative from encoding.com

        If any of the fields not specified, uses encoding.com defaults by not detailing it as part of the format data.
        Only key pertinent parts are always provisioned

        :param time: int
            time value represented in seconds
            time can also be represented in a percentage of the entire video length by providing ##%
            for example:  5% can be provided in the time string
        :param video_codec:
            video codec desired to encode for the thumbnail
        :param width: int

        :param keep_aspect_ratio:
        :param rotate:
        :param file_extension:

        :return: python dict representing all the keys set needed for thumbnail representation
        :rtype: dict
        """
        format = {
            'output': 'thumbnail',
            'file_extension': file_extension,
            'keep_aspect_ratio': 'yes' if keep_aspect_ratio else 'no'
        }
        if time:
            format['time'] = time
        if video_codec:
            format['video_codec'] = video_codec
        if width:
            format['width'] = width
        if rotate:
            format['rotate'] = rotate

        return format
