from __future__ import absolute_import, print_function, division
import pandas as pd

from config import (DataConfig)

__all__ = [
    'Menu', 'Ingredient', 'Seasoning'
]

# TODO: set `datetime_format` by reading from config file
DT_FMT = 'yyyy/MM/dd'   # datetime_format
UT_FACTOR = 1000000000

class XlsxFile(object):
    def __init__(self):
        self.df = None

    @classmethod
    def from_excel(clz, fpath):
        try:
            xlsx = clz()
            xlsx.df = pd.read_excel(fpath)
        except:
            raise
        return xlsx

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
    """
    @attr config : configurations and settings of menu
    @attr dlist : list of dishes
    """
    def __init__(self):
        super(Menu, self).__init__()
        self.config = DataConfig().menu
        self.dlist = []

    @classmethod
    def from_excel(clz, fpath):
        obj = super(Menu, clz).from_excel(fpath)
        obj._init_dlist()
        return obj

    def to_excel(self, opath):
        hd = self.config.header
        super(Menu, self).to_excel(opath, header=hd)

    def _remove_serial_num_of_header(self, delimiter='.'):
        # no matter `parts` can be splitted or not, it will be an list
        return [val.split(delimiter)[0] for val in self.df.columns]

    def _init_dlist(self):
        for i, row in self.df.iterrows():
            # truncate unix timestamp to second
            k = row[self.config.k_date].value // UT_FACTOR

            # use unix timestamp as key
            dishes = Dishes(date=k)
            dishes.parse(row, self.config.k_dishes)
            self.dlist.append(dishes)

    def build_ingredient_dataframe(self):
        return [Ingredient.from_daily_menu(val) for val in self.dlist]

    def export_ingredient_sheet(self, fname='ingr'):
        sheets = self.build_ingredient_dataframe()
        for sh in sheets:
            sh.to_excel('ingr_{0}.xlsx'.format(sh.date))


class Ingredient(XlsxFile):
    def __init__(self, date=None):
        super(Ingredient, self).__init__()
        self.config = DataConfig().ingredient
        self.date = date

    @classmethod
    def from_daily_menu(clz, daily_menu):
        ingr = Ingredient(date=daily_menu.date)

        # set default values for dateframe
        dv = ingr.config.default_values.copy()
        dv[ingr.config.k_date] = pd.to_datetime(ingr.date, unit='s')

        # preallocate space for daily menu
        size = daily_menu.count_ingr()
        df = pd.DataFrame(dv, index=range(size))

        # fill content of dishes
        cnt = 0
        ingr_list = daily_menu.to_list()
        for val in ingr_list:
            df.loc[cnt, ingr.config.k_dish] = val[0]
            df.loc[cnt, ingr.config.k_ingr] = val[1]
            cnt += 1

        # reorder header
        ingr.df = df.reindex_axis(ingr.config.header, axis=1)
        return ingr

    def to_excel(self, opath):
        super(Ingredient, self).to_excel(opath)


class Seasoning(XlsxFile):
    def __init__(self):
        super(Seasoning, self).__init__()
        self.config = DataConfig().seasoning

    def to_excel(self, opath):
        super(Seasoning, self).to_excel(opath)


class Dish(dict):
    """
    @attr name : Name of dish
    @attr ingr : Ingredients of dish
    """
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.ingr = kwargs.pop('ingr', [])
        super(Dish, self).__init__({self.name: self.ingr})

    def expand(self):
        """
        Returns
        -------
        out : list of tuples
            Name of this dish and ingredients.

        Example
        -------
        >>> dish = Dish(name='corn_soup', ingr=['corn', 'butter', 'egg'])
        >>> print(dish.expand())
        ['corn_soup', 'corn']
        ['corn_soup', 'butter']
        ['corn_soup', 'egg']
        """
        ingr_list = [''] if len(self.ingr) == 0 else self.ingr
        return [(self.name, v) for v in ingr_list]


class Dishes(list):
    """
    List of dishes with assigned date.

    @attr date : Assigned date of these dishes.
    """
    def __init__(self, *args, **kwargs):
        self.date = kwargs.pop('date')
        super(Dishes, self).__init__(*args, **kwargs)

    def parse(self, src, desired):
        """
        Parameters
        ----------
        src : pandas.core.series.Series
            Srouce to be parsed.
        desired : list
            Keys of desired dishes to be parsed.
        """
        parsed = [Dish(name=src[k]) for k in desired]
        self.extend(parsed)

    def count_ingr(self, cnt_empty_list=True):
        # get length of ingredients of each dish
        lens = map(len, [v[v.name] for v in self])

        if cnt_empty_list == True:
            lens = map(lambda x: 1 if x == 0 else x, lens)
        return sum(lens)

    def to_list(self):
        """
        Returns
        -------
        out : list of tuples
            Each tuple contains name and ingredients of corresponding dish.
        """
        return [name_ingr for dish in self for name_ingr in dish.expand()]
