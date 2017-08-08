from __future__ import absolute_import, print_function, division
import pandas as pd

DT_FMT = 'yyyy/MM/dd'   # datetime_format

class Menu(object):
    def __init__(self):
        self.df = None

    def from_excel(self, fpath):
        try:
            self.df = pd.read_excel(fpath)
        except:
            raise

    def to_excel(self, opath, columns=None):
        writer = pd.ExcelWriter(opath, datetime_format=DT_FMT)
        if columns is not None:
            # Some of `df.column`s might be appended with suffixes if there are duplicate names. 
            # If users do't want the modified column names, they can overwrite them by giving `columns`.
            temp = self.df.copy()
            temp.columns = columns
            temp.to_excel(writer, index=False)
        else:
            self.df.to_excel(writer, index=False)
        writer.save()
