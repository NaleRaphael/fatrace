from __future__ import absolute_import, print_function, division
import os.path
import traceback

import pandas as pd
import config

from core import XlsxFile, Menu, Ingredient, Seasoning

def main(fpath):
    menu = Menu()
    menu.from_excel(fpath)
    menu.to_excel('test.xlsx')

def config_test():
    dconf = config.DataConfig()

def build_table_from_menu(fpath):
    menu = Menu()
    ingr = Ingredient()
    menu.from_excel(fpath)
    menu.build_ingredient_row(ingr)
    print(menu)

if __name__ == '__main__':
    try:
        fpath = r'data\menu\menu_mul.xlsx'

        # main(fpath)
        # config_test()
        build_table_from_menu(fpath)
    except Exception:
        traceback.print_exc()
