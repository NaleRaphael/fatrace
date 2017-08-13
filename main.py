from __future__ import absolute_import, print_function, division
import os.path
import traceback
from pprint import pprint

import pandas as pd
import config

from core import XlsxFile, Menu

def main(fpath):
    menu = Menu()
    menu.from_excel(fpath)
    menu.to_excel('test.xlsx')

def config_test():
    opath = r'D:\Users\Nale\Documents\Bitbucket\fatrace\converter_config.json'
    conf = config.DataConfig()
    data = conf.load(opath)
    pprint(data)

    # conf_menu = config.MenuConfig()
    # conf_menu.header = ['school', 'dish1', 'dish2', 'dish3']

    # conf.menu = conf_menu
    # conf.export(opath)


if __name__ == '__main__':
    try:
        # fpath = r'data\menu\menu_20170626.xlsx'
        # main(fpath)
        config_test()
    except Exception:
        traceback.print_exc()
