from __future__ import absolute_import
import json

class JsonObject(object):
    def get_dict(self):
        return self.__dict__

class DataConfig(object):
    def __init__(self, config_path=None):
        self.menu = MenuConfig()
        self.ingredient = IngredientConfig()
        self.seasoning = SeasoningConfig()
        if config_path is not None:
            self.config = json.loads(config_path)

    def export(self, opath):
        with open(opath, 'w') as ofile:
            json.dump(self.__dict__, ofile, 
                default=lambda o: o.__dict__, indent=4)

    def load(self, fpath):
        with open(fpath, 'r') as ifile:
            data =  json.load(ifile)
        return data

class MenuConfig(JsonObject):
    def __init__(self, header=None):
        self.header = header

class IngredientConfig(JsonObject):
    def __init__(self, header=None):
        self.header = header

class SeasoningConfig(JsonObject):
    def __init__(self, header):
        self.header = header



