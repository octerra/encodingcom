"""
Format handler for encoding.com


"""

from exceptions import InvalidParameterError


class Format(object):
    """
    class representation of "canned" format.
    Enables clients to build and store formats for reuse in differing encoding.com requests.

    Usage:
    flv_libx264 = Format()
    flv_libx264.video_codec = 'flv:libx264
    flv_libx264.blah =


    result = encoding.add_media(blah, flv_libx264)

    """

    @property
    def video_codec(self):
        return self._video_codec

    @video_codec.setter
    def video_codec(self, value: str):
        """
        :param value: str
            Video codec setting is a string comprised of a valid "codec type:encoder"
            For example:
            "mov:libx264" specifies an exact video codec and libx264 encoder used for mov format.
            "mov" without a explicit encoder specification results in using the default format used for "mov".
                In this case, the default is "mpeg4"

        :return: None
        """
        valid_video_codec = {
            'flv': {'flv': '', 'libx264': '', 'vp6': ''},
            'fl9': {'libx264': ''},
            'wmv': {'wmv2': '', 'msmpeg4': ''},
            'zune': {'wmv2': '', 'msmpeg4': ''},
            '3gp': {'h263': '', 'mpeg4': '', 'libx264': ''},
            'android': {'h263': '', 'mpeg4': '', 'libx264': ''},
            'm4v': {'mpeg4': ''},
            'ipod': {'mpeg4': '', 'libx264': ''},
            'iphone': {'mpeg4': '', 'libx264': ''},
            'appletv': {'mpeg4': '', 'libx264': ''},
            'psp': {'mpeg4': '', 'libx264': ''},
            'mp4': {'mpeg4': '', 'libx264': '', 'hevc': ''},
            'ogg': {'libtheora': ''},
            'webm': {'libvpx': ''},
            'mp3': {},
            'wma': {},
            'mpeg2': {'mpeg2video': ''},
            'mpeg1': {'mpeg1video': ''},
            'mov': {'mpeg4': '', 'libx264': '', 'xdcam': '', 'dvcpro': '', 'dvcpro50': '', 'dvcprohd': '', 'mjpeg': ''},
            'mpegts': {'libx264': '', 'mpeg2video': ''},
            'mxf': {'dvcpro': '', 'dvcpro50': '', 'dvcprohd': '', 'xdcamhd422': ''}
        }

        parts = value.split(':')
        if 1 == len(parts):
            # use the default format
            if value not in valid_video_codec:
                raise InvalidParameterError(value)
        elif 2 == len(parts):
            encoder_type = parts[0]
            encoder = parts[1]
            try:
                result = valid_video_codec[encoder_type][encoder]
            except KeyError:
                raise InvalidParameterError(value)
        else:
            raise InvalidParameterError('Incorrect video codec parameter designation')