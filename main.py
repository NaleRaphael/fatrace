from __future__ import absolute_import, print_function, division
import os.path
import traceback

import pandas as pd
import config

from core import XlsxFile, Menu

def main(fpath):
    menu = Menu()
    menu.from_excel(fpath)
    menu.to_excel('test.xlsx')

def config_test():
    dconf = config.DataConfig()

def build_table_from_menu():
    menu = Menu()

if __name__ == '__main__':
    try:
        fpath = r'data\menu\menu_20170626.xlsx'

        # main(fpath)
        # config_test()
        build_table_from_menu()
    except Exception:
        traceback.print_exc()
