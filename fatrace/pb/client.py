from __future__ import absolute_import, print_function

import grpc

from .core_pb2 import Ingr, Dish, DBMsg
from .core_pb2_grpc import IngrDBManagerStub

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = IngrDBManagerStub(channel)
    ingr01 = Ingr(name='carrot', weight=5.0)
    ingr02 = Ingr(name='beef', weight=2.8)
    dish = Dish(name='test_dish', ingrs=[ingr01, ingr02])
    response = stub.Insert(dish)
    print(response.is_updated)

if __name__ == '__main__':
    run()
