from __future__ import absolute_import, print_function, division
import os.path
import traceback

import pandas as pd
import config

from core import Menu, Ingredient, Seasoning, Dishes

def main(fpath):
    menu = Menu()
    menu.from_excel(fpath)
    menu.to_excel('test.xlsx')

def config_test():
    dconf = config.DataConfig()

def build_table_from_menu(fpath):
    menu = Menu.from_excel(fpath)
    menu.export_ingredient_sheet()

def dish_test(fpath):
    menu = Menu.from_excel(fpath)
    dish = Dishes(date=1).parse(menu.df.loc[0], menu.config.k_dishes)
    print(dish)


if __name__ == '__main__':
    try:
        fpath = r'data\menu\menu_mul.xlsx'

        # main(fpath)
        # config_test()
        build_table_from_menu(fpath)
        # dish_test(fpath)
    except Exception:
        traceback.print_exc()
