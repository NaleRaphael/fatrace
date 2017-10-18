from __future__ import absolute_import

import sys

from fatrace.pb.core_pb2 import (
    DBMsg, 
)
from fatrace.pb.core_pb2_grpc import (
    IngrDBManagerServicer, EchoerServicer, FatraceEditorServicer, 
    TesterServicer
)
from fatrace.pb.converter import PBConverter
from fatrace.core import (
    IngredientDB, MenuSheet, IngredientSheet, DailyMenu, Dish
)

_ONE_DAY_IN_SECONDS = 60*60*24
_INGR_DB_PATH = 'db_ingr.json'

__all__ = ['IngrDBManager', 'Echoer', 'FatraceEditor', 'Tester']

class IngrDBManager(IngrDBManagerServicer):
    # TODO: improve this
    def Insert(self, request, context):
        obj = PBConverter.toDish(request)
        db = IngredientDB(_INGR_DB_PATH)
        res = db.insert(obj.name, obj.ingrs)
        if res:
            db.export(_INGR_DB_PATH)
            print('database is updated')
        else:
            print('failed to insert value')
        return DBMsg(is_updated=res)


class Echoer(EchoerServicer):
    def Echo(self, request, context):
        print('server: {0}'.format(request.content))
        return request

    def GhostEcho(self, request, context):
        print('server: beeeeeeeeeeeee')
        return request


class FatraceEditor(FatraceEditorServicer):
    def GetMenu(self, request, context):
        pass


class Tester(TesterServicer):
    def testIngr(self, request, context):
        obj = PBConverter.toIngr(request)
        print('convert from requeset: {0}'.format(obj))
        res = PBConverter.fromIngr(obj)
        print('convert back: {0}'.format(res))
        return res

    def testDish(self, request, context):
        obj = PBConverter.toDish(request)
        print('convert from requeset: {0}'.format(obj))
        res = PBConverter.fromDish(obj)
        print('convert back: {0}'.format(res))
        return res

    def testMenu(self, request, context):
        pass