from __future__ import absolute_import, print_function, division
import pandas as pd
import json

from .config import DataConfig
from .io import JsonWriter

__all__ = [
    'Menu', 'Ingredient', 'Seasoning', 'Dish', 'DailyMenu', 'IngredientDB'
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
    @attr dmlist : list of daily menu
    """
    def __init__(self):
        super(Menu, self).__init__()
        self.config = DataConfig().menu
        self.dmlist = []

    @classmethod
    def from_excel(clz, fpath, db=None):
        obj = super(Menu, clz).from_excel(fpath)
        obj._init_dmlist(db=db)
        return obj

    def to_excel(self, opath):
        hd = self.config.header
        super(Menu, self).to_excel(opath, header=hd)

    def _remove_serial_num_of_header(self, delimiter='.'):
        # no matter `parts` can be splitted or not, it will be an list
        return [val.split(delimiter)[0] for val in self.df.columns]

    def _init_dmlist(self, db=None):
        for i, row in self.df.iterrows():
            # truncate unix timestamp to second
            k = row[self.config.k_date].value // UT_FACTOR

            # use unix timestamp as key
            dm = DailyMenu(date=k)
            dm.parse_from_menu(row, self.config.k_dishes, db=db)
            self.dmlist.append(dm)

    def build_ingredient_dataframe(self):
        return [Ingredient.from_daily_menu(val) for val in self.dmlist]

    def export_ingredient_sheet(self, fname='ingr'):
        sheets = self.build_ingredient_dataframe()
        for sh in sheets:
            sh.to_excel('ingr_{0}.xlsx'.format(sh.date))


class Ingredient(XlsxFile):
    def __init__(self, date=None):
        super(Ingredient, self).__init__()
        self.config = DataConfig().ingredient
        self.date = date
        self.dishes = None

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

    @classmethod
    def from_excel(clz, fpath):
        obj = super(Ingredient, clz).from_excel(fpath)
        obj._set_date()
        obj._init_dishes()
        return obj

    def to_excel(self, opath):
        super(Ingredient, self).to_excel(opath)

    def _set_date(self):
        try:
            self.date = self.df.loc[0, self.config.k_date]
        except:
            raise

    def _init_dishes(self):
        self.dishes = DailyMenu(date=self.date)

        d = {}
        for i, row in self.df.iterrows():
            key = row[self.config.k_dish]
            if key not in d:
                d[key] = []
            d[key].append(row[self.config.k_ingr])

        self.dishes.from_dict(d)


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
        Expand object content into list in the format of `[dish_name, ingredient]`.

        Returns
        -------
        out : list of tuples
            Name of this dish and ingredients.

        Example
        -------
        >>> dish = Dish(name='corn_soup', ingr=['corn', 'butter', 'egg'])
        >>> print(dish.expand())
        [['corn_soup', 'corn'],
        ['corn_soup', 'butter'],
        ['corn_soup', 'egg']]
        """
        ingr_list = [''] if len(self.ingr) == 0 else self.ingr
        return [(self.name, v) for v in ingr_list]


class DailyMenu(list):
    """
    List of dishes with assigned date.

    @attr date : Assigned date of these dishes.
    """
    def __init__(self, *args, **kwargs):
        self.date = kwargs.pop('date')
        super(DailyMenu, self).__init__(*args, **kwargs)

    def parse_from_menu(self, src, desired, db=None):
        """
        Parameters
        ----------
        src : pandas.core.series.Series
            Source to be parsed.
        desired : list
            Keys of desired dishes to be parsed.
        db : IngredientDB
            Database for searching ingredients of dish.
        """
        if type(db) is not IngredientDB:
            raise TypeError('Type of `db` should be `IngredientDB`.')
        if db is not None:
            parsed = [Dish(name=src[k], ingr=db.query(src[k])) for k in desired]
        else:
            parsed = [Dish(name=src[k]) for k in desired]
        self.extend(parsed)

    def from_dict(self, d):
        self.extend([Dish(name=k, ingr=d[k]) for k in d])

    def count_ingr(self, cnt_empty_list=True):
        # get length of ingredients of each dish
        lens = map(len, [v.ingr for v in self])

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


class IngredientDB(dict):
    __single = None
    __initialized = False

    def __new__(clz, *args, **kwargs):
        if IngredientDB.__single is None:
            IngredientDB.__single = dict.__new__(clz)
        return IngredientDB.__single

    def __init__(self, fpath):
        if IngredientDB.__initialized: return
        self.load(fpath)
        IngredientDB.__initialized = True

    def load(self, fpath):
        with open(fpath, 'r') as ifile:
            super(IngredientDB, self).__init__(json.load(ifile))

    def export(self, fpath):
        try:
            JsonWriter.export(self, fpath)
        except:
            raise

    @classmethod
    def collect(clz, ingr_dir, ingr_pattern, load_right_away=False,
                dbname='db_ingr', dupname='duplicate_ingr'):
        import os
        import glob
        sheets = glob.glob(os.path.join(ingr_dir, ingr_pattern))
        data = {}
        duplicate = []
        for fp in sheets:
            ingr = Ingredient.from_excel(fp)
            for dish in ingr.dishes:
                if dish.name in data:
                    duplicate.append(data)
                else:
                    data[dish.name] = dish.ingr

        JsonWriter.export(data, '{0}.json'.format(dbname))
        JsonWriter.export(duplicate, '{0}.json'.format(dupname))

        if load_right_away:
            obj = clz()
            obj.__dict__ = data
            return obj

    def query(self, key):
        return self.get(key, [])

    def insert(self, key, val, overwrite=False, ori_encodig='utf-8'):
        """
        Parameters
        ----------
        key : string
            Key of item to be inserted.
        val : list
            Value of item.
        overwrite : bool
            Overwrite existing value if the key has already in database.

        Returns
        -------
        isSuccess : bool
            If item is added successfully, return true. Otherwise, return false.
        """
        if type(val) is not list:
            raise TypeError('Given `val` should be a list.')
        key = key.decode(ori_encodig)
        val = [v.decode(ori_encodig) for v in val]
        is_exist = key in self
        if not is_exist or (is_exist and overwrite):
            self[key] = val
            return True
        else:
            return False
