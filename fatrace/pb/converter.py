from __future__ import absolute_import, print_function

from fatrace.pb import core_pb2 as pbdef
from fatrace.core import objbase as pydef


class PBConverter(object):
    @classmethod
    def _type_check(clz, x, desired_type):
        if type(x) is not desired_type:
            raise PBTypeError(type(desired_type))

    @classmethod
    def toIngr(clz, x):
        """Convert `pbdef.Ingredient` to `pydef.Ingredient`."""
        clz._type_check(x, pbdef.Ingredient)
        return pydef.Ingredient(name=x.name, weight=x.weight)

    @classmethod
    def fromIngr(clz, x):
        """Convert `pydef.Ingredient` to `pbdef.Ingredient`."""
        clz._type_check(x, pydef.Ingredient)
        obj = pbdef.Ingredient()
        obj.name = x.name
        obj.weight = x.weight
        return obj

    @classmethod
    def toDish(clz, x):
        """Convert `pbdef.Dish` to `pydef.Dish`."""
        clz._type_check(x, pbdef.Dish)
        obj = pydef.Dish(name=x.name, ingrs=[clz.toIngr(v) for v in x.ingrs])
        return obj

    @classmethod
    def fromDish(clz, x):
        """Convert `pydef.Dish` to `pbdef.Dish`."""
        clz._type_check(x, pydef.Dish)
        obj = pbdef.Dish()
        obj.name = x.name
        obj.ingrs.extend([clz.fromIngr(v) for v in x.ingrs])
        return obj

    @classmethod
    def toDailyMenu(clz, x):
        """Convert `pbdef.DailyMenu` to `pydef.DailyMenu`"""
        clz._type_check(x, pbdef.DailyMenu)
        dishes = [clz.toDish(v) for v in x.dishes]
        date_serve = x.date
        raise NotImplementedError()


class PBTypeError(TypeError):
    def __init__(self, desired_type):
        super(TypeError, self).__init__()
        self.message += ' Type of input should be {0}'.format(type(desired_type))
