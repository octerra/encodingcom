#! /usr/bin/env python
"""
Monitor the job status for a given mediaid, or the latest mediaid job in the queue.

If the job has finished or exited, the last known state (Finished, Error, Stopped) is reflected.
Otherwise it will monitor and report the state until in a completed success/error state of the job

USAGE:
    python job_status_monitor --user=1234 --key=abcde

    python job_status_monitor --user=1234 --key=abcde > output.json

    flags:
    --user: Required
        Designates the user id associated with client encoding.com account

    --key: Required
        Designates the user access key associated with client encoding.com account

    ----mediaid: Optional
        Designates the mediaid desired to track status of.
        This is dynamically assigned by Encoding.com via AddMedia or AddMediaBenchMark.
        If left empty, uses the latest encoding.com mediaid designated in the queue

"""

from argparse import ArgumentParser, Namespace
from pprint import PrettyPrinter

from encodingcom.encoding import Encoding
from encodingcom.encoding_utils import get_latest_media
from encodingcom.poller import Poller


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

        '--interval': {
            'required': False,
            'help': 'Designates an interval to poll encoding.com for the job status details (in seconds)\n'
                    'Defaults to 5 seconds if not specified'
        }

    }

    parser = ArgumentParser()
    for argument in arguments.keys():
        parser.add_argument(argument, help=arguments[argument]['help'], required=arguments[argument]['required'])

    args = parser.parse_args()

    if not args.mediaid:
        # not specified... reflect as this will use the latest encoding mediaid later in the workflow
        args.mediaid = ''

    if not args.interval:
        args.interval = 5

    return args


def pretty_print_response(**kwargs):
    """
    Use Python standard pprint to output to a nice formatted response from the differing status calls

    :param: **kwargs
        Key items in the kwargs:
        media_id: MediaID associated with the Job
        status: Status / state of the job
        response:
    :return:
    """
    print('\nMedia ID: %s' % kwargs['media_id'])
    print(' ==== Status: %s =====' % kwargs['status'])

    pretty = PrettyPrinter()
    pretty.pprint(kwargs['response'])


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
        print('MediaId not specified, using the latest media id in the queue: %s' % media_id)

    Poller.poll_status(encoding, media_id=media_id, callback=pretty_print_response,
                       interval=float(args_dict['interval']))


if __name__ == '__main__':

    args = get_args()
    main(args)