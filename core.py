from __future__ import absolute_import, print_function, division
import pandas as pd

from config import (MenuConfig, IngredientConfig, SeasoningConfig, DataConfig)

__all__ = [
    'Menu', 'Ingredient', 'Seasoning'
]

# TODO: set `datetime_format` by reading from config file
DT_FMT = 'yyyy/MM/dd'   # datetime_format


class XlsxFile(object):
    def __init__(self):
        self.df = None

    def from_excel(self, fpath):
        try:
            self.df = pd.read_excel(fpath)
        except:
            raise

    def to_excel(self, opath, header=None):
        """
        Parameters
        ----------
        opath : string
            Output path.
        header : array_like
            Column names to be written.

        Note
        ----
        Some of `df.columns` might be appended with suffixes if there are duplicate names.
        If users don't want the modified column names, they can overwrite them by giving `header`.
        """
        writer = pd.ExcelWriter(opath, datetime_format=DT_FMT)
        self.df.to_excel(writer, index=False)
        if header is not None:
            pd.DataFrame(header).transpose().to_excel(writer, index=False, header=False, startrow=0)
        writer.save()


class Menu(XlsxFile):
    def __init__(self):
        super(Menu, self).__init__()
        self.config = DataConfig().menu

    def to_excel(self, opath):
        hd = self.config.header
        super(Menu, self).to_excel(opath, header=hd)

    def _remove_serial_num_of_header(self, delimiter='.'):
        # no matter `parts` can be splitted or not, it will be an list
        return [val.split(delimiter)[0] for val in self.df.columns]

    def build_ingredient_row(self, obj_ingr):
        hd_ingr = obj_ingr.config.header
        df_ingr = pd.DataFrame(columns=hd_ingr)
        mi = self.config.map2ingr

        for i in range(self.df.index.size):
            pass
            # new_row = {mi[k]: self.df.ix[[i]][k].values for k in mi}
            # [nr[mi[k]].append(self.df.ix[[i]][k].values) if k in nr 
            #  else nr.update({mi[k]: self.df.ix[[i]][k].values}) for k in mi]
#        result = self.df.append([], ignore_index=True)

class Ingredient(XlsxFile):
    def __init__(self):
        super(Ingredient, self).__init__()
        self.config = DataConfig().ingredient

    def to_excel(self, opath):
        # TODO: export individual files according to date
        super(Ingredient, self).to_excel(opath)

class Seasoning(XlsxFile):
    def __init__(self):
        super(Seasoning, self).__init__()
        self.config = DataConfig().seasoning

    def to_excel(self, opath):
        super(Seasoning, self).to_excel(opath)
