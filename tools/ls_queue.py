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
from pprint import PrettyPrinter

from encodingcom.encoding import Encoding
from encodingcom.exception import EncodingErrors
from encodingcom.response_helper import get_response


def pretty_print_response(data: dict):
    """
    Use Python standard pprint to output to a nice formatted response from the differing status calls

    :param: **kwargs
        Key items in the kwargs:
        media_id: MediaID associated with the Job
        status: Status / state of the job
        response:
    :return:
    """

    pretty = PrettyPrinter()
    pretty.pprint(data)


def get_args() -> Namespace:
    """

    :return: Arguments parsed from the ArgumentParser
    :rtype: Namespace
    """

    arguments = {
        '--verbose': {
            'required': False,
            'help': 'Verbose mode is enabled... '
                    'Status to represent the mediaid id dispatched to latest status information'
                    'If not specified, verbose is disabled'
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

    if not args.verbose:
        # not specified... reflect as this will use the latest encoding mediaid later in the workflow
        args.verbose = False

    return args


def verbose_report(encoding: Encoding):
    """
    Verbose mode reporting of media id and its contents by dispatching a GetStatus action and organizing the report
    contents into mediaid buckets

    :return:
    """
    print('Verbose mode enabled, GetStatus for each of the mediaid reported:')

    pretty = PrettyPrinter()

    status, response = encoding.get_media_list()
    response = get_response(response)

    for media in response['media']:
        try:
            output = {}
            output[media['mediaid']] = media
            pretty.pprint(output)

            status, status_reponse = encoding.get_status(mediaid=media['mediaid'])
            print('Status for mediaid: %s' % media['mediaid'])
            pretty.pprint(status_reponse)

            status, media_info_response = encoding.get_media_info(extended=True, mediaid=media['mediaid'])
            print('MediaInfo (extended) for mediaid: %s' % media['mediaid'])
            pretty.pprint(media_info_response)

            print('\n')

        except EncodingErrors as ex:
            print('*** Encoding Error Found!: %s' % str(ex))


def main(args: Namespace):
    """
    Main entry point used as a stand alone python execution

    :param args: Namespace
        arguments from the arguments parser
    :return:
    """

    args_dict = vars(args)

    encoding = Encoding(user_id=args_dict['user'], user_key=args_dict['key'])

    if args_dict['verbose']:
        verbose_report(encoding)
    else:
        status, response = encoding.get_media_list()
        if 200 == status:
            pretty_print_response(get_response(response))
        else:
            print('HTTP error returned: %s' % status)


if __name__ == '__main__':

    args = get_args()
    main(args)