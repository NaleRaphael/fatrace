from __future__ import absolute_import, print_function

import grpc

from .core_pb2 import Ingredient, Dish, DBMsg
from .core_pb2_grpc import IngrDBManagerStub
from .core_pb2 import Foo
from .core_pb2_grpc import EchoerStub


def ingrdb_insert():
    channel = grpc.insecure_channel('localhost:50051')
    stub = IngrDBManagerStub(channel)
    ingr01 = Ingredient(name='carrot', weight=5.0)
    ingr02 = Ingredient(name='beef', weight=2.8)
    dish = Dish(name='test_dish', ingrs=[ingr01, ingr02])
    response = stub.insert(dish)
    print(response.is_updated)


def echo():
    channel = grpc.insecure_channel('localhost:50051')
    stub = EchoerStub(channel)
    res = stub.echo(Foo(content='Hi'))
    print('client: {0}'.format(res.content))


def get_menu():
    pass
