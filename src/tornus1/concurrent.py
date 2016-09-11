# -*- coding: utf-8 -*-
"""
(C) 2016 Ángel Olea Gómez   www.ovalo-software.com

Aisla un poco del tornado

---------------- ------------------------------------------
2016-09-11 17:02 - aolea - creation

"""
from tornado import gen
from tornado.ioloop import IOLoop

coroutine = gen.coroutine
Future = gen.Future


def resolve_future(future):
    """
    Devuelve el resultado de un future ejecutándolo dentro de un ioloop creado al efecto

    :param future:
    :return:
    """
    if not isinstance(future, Future):
        return future
    ioloop = IOLoop.instance()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    return future.result()

