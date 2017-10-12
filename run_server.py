from __future__ import absolute_import
from fatrace.pb import server

from argparse import ArgumentParser

func_entry = {
    'ingrdb': server.serve_ingrdb,
    'echo': server.serve_echo
}

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('entry', metavar='func_entry')

    try:
        args = parser.parse_args()
    except:
        raise
    return args


def main():
    args = parse_args()
    arg_dict = vars(args)
    try:
        if args.entry not in func_entry:
            print('No given entry: {0}'.format(args.entry))
        func_entry[args.entry]()
    except:
        raise


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex.message)
