#! /usr/bin/env python
"""
Cancel a specified mediaid job along with all its children.
Due to minimum documentation on encoding.com.

CancelMedia action invoked on a





Provided for the following purposes:
1.) CLI/API control of cancelling a specific mediaid job... use at your own risk.
2.) Support a function test workflow
3.) Education purposes as cancel media is unclear for jobs that are completed as this is undocumented.

USAGE:
    python cancel_media --user=1234 --key=abcde
    * Cancels the latest mediaid in the queue

    python cancel_media --user=1234 --key=abcde --mediaid=123
    * Cancels the mediaid with the value of 123


"""

from argparse import ArgumentParser, Namespace

from encodingcom.encoding import Encoding
from encodingcom.encoding_utils import get_latest_media


def get_args() -> Namespace:
    """

    :return: Arguments parsed from the ArgumentParser
    :rtype: Namespace
    """

    arguments = {
        '--mediaid': {
            'required': False,
            'help': 'Detail desired media id desired.  '
                    'If not specified, use the latest media in the job queue of encoding.com'
        },

        '--user': {
            'required': True,
            'help': 'Designate a required UserID needed to access encoding.com'
        },

        '--key': {
            'required': True,
            'help': 'Designate a required User Key to access encoding.com'
        },

    }

    parser = ArgumentParser()
    for argument in arguments.keys():
        parser.add_argument(argument, help=arguments[argument]['help'], required=arguments[argument]['required'])

    args = parser.parse_args()

    if not args.mediaid:
        # not specified... reflect as this will use the latest encoding mediaid later in the workflow
        args.mediaid = ''

    return args


def main(args: Namespace):
    """
    Main entry point used as a stand alone python execution

    :param args: Namespace
        arguments from the arguments parser
    :return:
    """

    args_dict = vars(args)

    encoding = Encoding(user_id=args_dict['user'], user_key=args_dict['key'])

    if args_dict['mediaid']:
        media_id = args_dict['mediaid']
    else:
        media_id = get_latest_media(encoding)['mediaid']
        print('MediaId not specified, cancelling the media id in the queue: %s' % media_id)

    encoding.cancel_media(mediaid=[media_id])


if __name__ == '__main__':

    args = get_args()
    main(args)