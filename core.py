from __future__ import absolute_import, print_function, division
import pandas as pd

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
    def to_excel(self, opath):
        hd = self._remove_serial_num_of_header()
        super(Menu, self).to_excel(opath, header=hd)

    def _remove_serial_num_of_header(self, delimiter='.'):
        hd = []
        for val in self.df.columns:
            parts = val.split(delimiter)
            # no matter `parts` can be splitted or not, it will be an list
            hd.append(parts[0])
        return hd

class Ingredient(XlsxFile):
    def to_excel(self, opath):
        super(Ingredient, self).to_excel(opath)

class Seasoning(XlsxFile):
    def to_excel(self, opath):
        super(Seasoning, self).to_excel(opath)
