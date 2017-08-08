import os.path
import traceback

import pandas as pd

def main(fn):
    df = pd.read_excel(fn)
    keys = df.keys()

    # TODO: set `datetime_format` by reading from config file
    writer = pd.ExcelWriter('output.xlsx', datetime_format='yyyy/MM/dd')
    df.to_excel(writer, index=False)
    writer.save()


if __name__ == '__main__':
    try:
        fn = r'data\menu\menu_20170626.xlsx'
        main(fn)
    except Exception:
        traceback.print_exc()
