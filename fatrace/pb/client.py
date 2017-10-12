from __future__ import absolute_import, print_function

import grpc

from .core_pb2 import Ingr, Dish, DBMsg
from .core_pb2_grpc import IngrDBManagerStub
from .core_pb2 import Foo
from .core_pb2_grpc import EchoerStub


def ingrdb_insert():
    channel = grpc.insecure_channel('localhost:50051')
    stub = IngrDBManagerStub(channel)
    ingr01 = Ingr(name='carrot', weight=5.0)
    ingr02 = Ingr(name='beef', weight=2.8)
    dish = Dish(name='test_dish', ingrs=[ingr01, ingr02])
    response = stub.Insert(dish)
    print(response.is_updated)


def echo():
    channel = grpc.insecure_channel('localhost:50051')
    stub = EchoerStub(channel)
    res = stub.Echo(Foo(content='Hi'))
    print('client: {0}'.format(res.content))
