from __future__ import absolute_import
from fatrace.pb import server

from argparse import ArgumentParser

SERVICER_DICT = {
    'ingrdb': 'IngrDBManager',
    'echo': 'Echoer'
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('servicer_name', metavar='servicer_name')

    try:
        args = parser.parse_args()
    except:
        raise
    return args


def main():
    args = parse_args()
    try:
        if args.servicer_name not in SERVICER_DICT:
            raise Exception('No given servicer: {0}'.format(args.servicer_name))
        else:
            servicer = SERVICER_DICT[args.servicer_name]
        service_manager = server.ServerManager()
        service_manager.start_service(servicer)
    except:
        raise


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex.message)
