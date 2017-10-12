from __future__ import absolute_import

import time

from concurrent import futures
import grpc

from fatrace.pb.core_pb2 import DBMsg
from fatrace.pb.core_pb2_grpc import IngrDBManagerServicer, add_IngrDBManagerServicer_to_server
from fatrace.pb.core_pb2 import Foo
from fatrace.pb.core_pb2_grpc import  EchoerServicer, add_EchoerServicer_to_server
from fatrace.core import IngredientDB
from fatrace.pb.converter import Converter

_ONE_DAY_IN_SECONDS = 60*60*24
_INGR_DB_PATH = 'db_ingr.json'

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
 

def serve_ingrdb():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_IngrDBManagerServicer_to_server(IngrDBManager(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('grpc server is running: serve_ingrdb')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def serve_echo():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_EchoerServicer_to_server(Echoer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('grpc server is running: serve_echo')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
