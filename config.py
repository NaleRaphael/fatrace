from __future__ import absolute_import
import json

class ConfigBase(object):
    def __init__(self, **kwargs):
        dv = kwargs.get('default_values')
        self.header = self._get_header(dv)
        self.default_values = self._get_default_values(dv)

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

class IngredientConfig(ConfigBase):
    def __init__(self, **kwargs):
        super(IngredientConfig, self).__init__(**kwargs)

class SeasoningConfig(ConfigBase):
    def __init__(self, **kwargs):
        super(SeasoningConfig, self).__init__(**kwargs)

class DataConfig(object):
    def __init__(self, config_path=None):
        self.menu = None
        self.ingredient = None
        self.seasoning = None
        if config_path is not None:
            self.config = json.loads(config_path)

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
