from __future__ import absolute_import, print_function

from .core_pb2 import Ingr, Dish, DBMsg
from .core_pb2_grpc import IngrDBManagerStub

from . import core_pb2 as corepb
from fatrace.core import Dish, DailyMenu

class Converter(object):
    @staticmethod
    def toDish(pbDish):
        if type(pbDish) is not corepb.Dish:
            raise TypeError('Type of given object should be corepb.Dish')
        obj = Dish(name=pbDish.name, ingr=[v.name for v in pbDish.ingrs])
        return obj
