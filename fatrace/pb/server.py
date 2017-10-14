from __future__ import absolute_import

import sys
import time
from concurrent import futures
import grpc

from fatrace.pb import servicer
from fatrace.pb import core_pb2_grpc

_ONE_DAY_IN_SECONDS = 60*60*24

class ServerManager(object):
    def __init__(self, *args, **kwargs):
        pass

    def _get_servicer(self, clz_name):
        try:
            clz = getattr(sys.modules[servicer.__name__], clz_name)
        except AttributeError as err_attr:
            err_attr.message += '(Desired servicer is not defined)'
            raise err_attr
        return clz

    def _get_helper_method(self, clz_servicer):
        clz_parent_name = clz_servicer.__bases__[0].__name__
        hm_name = 'add_{0}_to_server'.format(clz_parent_name)
        try:
            hm = getattr(sys.modules[core_pb2_grpc.__name__], hm_name)
        except AttributeError as err_attr:
            err_attr.message += '(Desired helper method is not defined)'
            raise err_attr
        return hm

    def start_service(self, clz_name):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        clz_servicer = self._get_servicer(clz_name)
        hm = self._get_helper_method(clz_servicer)

        # register service
        hm(clz_servicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print('grpc server is running: {0}'.format(clz_name))
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)
