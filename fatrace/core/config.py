from __future__ import absolute_import
import json

__all__ = [
    'MenuConfig', 'IngredientConfig', 'SeasoningConfig', 
    'DataConfig'
]

DEFAULT_CONFIG_PATH = r'converter_config.json'

class ConfigBase(object):
    def __init__(self, **kwargs):
        dv = kwargs.pop('default_values')
        self.header = self._get_header(dv)
        self.default_values = self._get_default_values(dv)
        self.misc = kwargs

    def load(self, fpath):
        with open(fpath, 'r') as ifile:
            self.__dict__ = json.load(ifile)

    def _get_header(self, dv):
        if dv is not None:
            return [val.keys()[0] for val in dv]

    def _get_default_values(self, dv):
        if dv is not None:
            return {k: val[k] for val in dv for k in val}


class MenuConfig(ConfigBase):
    def __init__(self, **kwargs):
        super(MenuConfig, self).__init__(**kwargs)
        # key (field name) of date
        self.k_date = self.misc.pop('k_date')
        # keys (field names) of dishes in dataframe
        self.k_dishes = self.misc.pop('k_dishes')


class IngredientConfig(ConfigBase):
    def __init__(self, **kwargs):
        super(IngredientConfig, self).__init__(**kwargs)
        self.k_date = self.misc.pop('k_date')
        self.k_dish = self.misc.pop('k_dish')
        self.k_ingr = self.misc.pop('k_ingr')
        self.k_weight = self.misc.pop('k_weight')


class SeasoningConfig(ConfigBase):
    def __init__(self, **kwargs):
        super(SeasoningConfig, self).__init__(**kwargs)


class DataConfig(object):
    __single = None
    __initialized = False

    def __new__(clz):
        if DataConfig.__single is None:
            DataConfig.__single = object.__new__(clz)
        return DataConfig.__single

    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        if DataConfig.__initialized: return
        DataConfig.__initialized = True
        self.menu = None
        self.ingredient = None
        self.seasoning = None
        if config_path is not None:
            self.load(config_path)

    def export(self, opath):
        with open(opath, 'w') as ofile:
            json.dump(self.__dict__, ofile, 
                default=lambda o: o.__dict__, indent=4)

    def load(self, fpath):
        with open(fpath, 'r') as ifile:
            parsed = json.load(ifile)
            self.menu = MenuConfig(**parsed['menu'])
            self.ingredient = IngredientConfig(**parsed['ingredient'])
            self.seasoning = SeasoningConfig(**parsed['seasoning'])
