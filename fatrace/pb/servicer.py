from __future__ import absolute_import

from fatrace.pb.core_pb2 import DBMsg
from fatrace.pb.core_pb2_grpc import IngrDBManagerServicer, EchoerServicer
from fatrace.pb.converter import Converter
from fatrace.core import IngredientDB

_ONE_DAY_IN_SECONDS = 60*60*24
_INGR_DB_PATH = 'db_ingr.json'

__all__ = ['IngrDBManager', 'Echoer']

class IngrDBManager(IngrDBManagerServicer):
    # TODO: improve this
    def Insert(self, request, context):
        obj = Converter.toDish(request)
        db = IngredientDB(_INGR_DB_PATH)
        res = db.insert(obj.name, obj.ingr)
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
