# -*- coding: utf-8 -*-
"""
(C) 2016 Ángel Olea Gómez   www.ovalo-software.com

Arranca la aplicación

---------------- ------------------------------------------
2016-09-08 21:48 - aolea - creation

"""
from pprint import pprint
import os

import momoko
import tornado
import tornado.escape
import tornado.ioloop
import tornado.web

from tornus1.concurrent import resolve_future
from tornus1.handlers import TObjectHandler
from tornus1.record import Record
from tornus1.tobject import TContext, TObjectTable

PATH = os.path.dirname(__file__)
DSN = 'postgres://postgres:postgres@localhost/tornus1_test'


class Tornus1App(tornado.web.Application):

    def __init__(self):

        settings = dict(
            template_path=os.path.join(PATH, 'web'),
            static_path=os.path.join(PATH, 'web', 'static'),
            debug=True
        )

        conn = momoko.Pool(DSN)
        resolve_future(conn)
        table = TObjectTable(conn, 'tobjects', Record)

        handlers = [
            (r"/(?P<path>.*)", TObjectHandler, {'table': table, 'views': 'record'}),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {})
        ]
        super().__init__(handlers, **settings)


if __name__ == "__main__":

    pprint('http://localhost:7777')
    Tornus1App().listen(7777)
    tornado.ioloop.IOLoop.current().start()





















# (r"/",                                    RecordHandler, config, 'records'),
# (r"/",                                    RecordHandler, config, 'records'),
# (r"/(?P<key0>\w*)",                       RecordHandler, config, 'record'),
# (r"/(?P<key0>\w*)/fields",                FieldHandler,  config, 'fields'),
# (r"/(?P<record_id>\w*)/fields/(?P<field_id>\w*)",  FieldHandler,  config, 'field'),
# (r"/(?P<key0>\w*)/actions",               ActionHandler, config, 'actions'),
# (r"/(?P<key0>\w*)/actions/(?P<key1>\w*)", ActionHandler, config, 'action'),

# (r"/menu", MainHandler),
# (r"/login", MainHandler),
# (r"/logout", MainHandler),
# (r"/profile", MainHandler),
#
# (r"/users", MainHandler),
# (r"/users/(.*)", MainHandler),
# (r"/users/(.*)/groups", MainHandler),
# (r"/users/(.*)/groups/(.*)", MainHandler),
#
# (r"/groups", MainHandler),
# (r"/groups/(.*)", MainHandler),
# (r"/groups/(.*)/users", MainHandler),
# (r"/groups/(.*)/users/(.*)", MainHandler),
#
# (r"/records", Thandler(Records(List))),
# (r"/records/(.*)", MainHandler),
# (r"/records/(.*)/fields", MainHandler),
# (r"/records/(.*)/fields/(.*)", MainHandler),
# (r"/records/(.*)/actions", MainHandler),
# (r"/records/(.*)/actions/(.*)", MainHandler),
# (r"/records/(.*)/actions/(.*)/steps", MainHandler),
# (r"/records/(.*)/actions/(.*)/steps/(.*)", MainHandler),
#
# (r"/data/(.*)", MainHandler),
# (r"/data/(.*)/(.*)", MainHandler),
# (r"/data/(.*)/(.*)/(.*)", MainHandler),
