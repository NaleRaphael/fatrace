from __future__ import absolute_import, print_function, division
import traceback

from fatrace.core import config
from fatrace.core import Menu, IngredientDB

def main(fpath):
    menu = Menu()
    menu.from_excel(fpath)
    menu.to_excel('test.xlsx')

def config_test():
    dconf = config.DataConfig()
    print(dconf)

def build_table_from_menu(fpath, dbpath):
    ingrdb = IngredientDB(dbpath)
    menu = Menu.from_excel(fpath, db=ingrdb)
    menu.export_ingredient_sheet()

def db_test(dbpath):
    ingrdb = IngredientDB(dbpath)
    print(ingrdb)

if __name__ == '__main__':
    try:
        fpath = r'data\menu\menu_mul.xlsx'
        dbpath = r'db_ingr.json'

        # main(fpath)
        # config_test()
        build_table_from_menu(fpath, dbpath)
        # db_test(dbpath)
    except Exception:
        traceback.print_exc()
