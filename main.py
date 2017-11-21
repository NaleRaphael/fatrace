from __future__ import absolute_import, print_function, division
from argparse import ArgumentParser
import os
import traceback

from fatrace.core import MenuSheet, IngredientDB

CHECK_BIG5_PARSE = ['fpath', 'odir']
CHECK_BIG5_UPDATEDB = ['name']


def parse_args():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(help='command', dest='cmd')
    sp_parse = subparser.add_parser('parse')
    sp_updatedb = subparser.add_parser('update_db')

    sp_parse.add_argument('-f', dest='fpath', metavar='input_file', 
                          help='path of input file')
    sp_parse.add_argument('-o', nargs='?', dest='odir', metavar='out_dir', 
                          default='', help='path of output directory')
    sp_parse.add_argument('--db', dest='dbpath', metavar='dbpath', 
                          default='db_ingr.json')

    sp_updatedb.add_argument('-d', dest='name', 
                             metavar='dish_name', type=str, 
                             default=None)
    sp_updatedb.add_argument('-i', nargs='+', dest='ingr', 
                             metavar='dish_ingr', 
                             default=[])
    sp_updatedb.add_argument('--db', dest='dbpath', metavar='dbpath', 
                             default='db_ingr.json')

    try:
        args = parser.parse_args()
    except:
        raise
    return args


def build_table_from_menu(**kwargs):
    if os.name == 'nt':
        for k in CHECK_BIG5_PARSE:
            if kwargs[k] != None:
                kwargs[k] = unicode(kwargs[k], 'big5')

    fpath = kwargs.pop('fpath')
    dbpath = kwargs.pop('dbpath')
    odir = kwargs.pop('odir')

    ingrdb = IngredientDB(dbpath) 
    menu = MenuSheet.from_excel(fpath, db=ingrdb)
    menu.export_ingredient_sheet(odir=odir)
    print('Ingredient sheets are generated sucessfully, '
          'they are under the folder: {0}'.format(os.path.abspath(odir)))


def update_ingr_database(**kwargs):
    if os.name == 'nt':
        for k in CHECK_BIG5_UPDATEDB:
            if kwargs[k] != None:
                kwargs[k] = unicode(kwargs[k], 'big5')

    dbpath = kwargs.pop('dbpath')
    name = kwargs.pop('name')
    ingr = kwargs.pop('ingr')
    print('name: {0}'.format(name))
    print('ingr: {0}'.format(ingr))

    ingrdb = IngredientDB(dbpath)
    is_sucessful = ingrdb.insert(name, ingr)
    if is_sucessful:
        ingrdb.save()
        print('Database is updated!')
    else:
        print('Failed to update database...')


FUNC_ENTRY = {
    'parse': build_table_from_menu, 
    'update_db': update_ingr_database
}
def main():
    args = parse_args()
    arg_dict = vars(args)
    try:
        if args.cmd not in FUNC_ENTRY:
            raise Exception('Given command is not valid: {0}'.format(args.cmd))
    except:
        raise

    try:
#        print(args)
#        return
        FUNC_ENTRY[args.cmd](**arg_dict)
    except:
        raise


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex.message)
        traceback.print_exc()
