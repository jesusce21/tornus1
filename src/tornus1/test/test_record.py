# -*- coding: utf-8 -*-
"""
(C) 2016 Ángel Olea Gómez   www.ovalo-software.com

#FIXME description

---------------- ------------------------------------------
2016-09-11 16:42 - aolea - creation

"""
import os
from pprint import pprint
import unittest
import momoko

from tornus1.concurrent import resolve_future
from tornus1.record import Record
from tornus1.tobject import TObject, AttrString, TContext, TComponent, TObjectTable


class RecordTestCase(unittest.TestCase):

    DSN = os.environ.get('DSN_TORNUS1_TEST') or 'postgres://postgres:postgres@localhost'

    # @classmethod
    # def setUpClass(cls):
    #     pool = momoko.Pool(cls.DSN)
    #     pool = resolve_future(pool.connect())
    #     resolve_future(pool.execute('drop database if exists tornus1_tests'))
    #     resolve_future(pool.execute('create database tornus1_tests'))
    #     pool.close()
    #     pool = momoko.Pool(cls.DSN + '/tornus1_tests')
    #     pool = resolve_future(pool.connect())
    #     with open('../database.sql', 'r') as f:
    #         resolve_future(pool.execute(f.read()))
    #     pool.close()

    def setUp(self):
        super().setUp()
        pool = momoko.Pool(self.DSN + '/tornus1_tests')
        resolve_future(pool.connect())
        self.pool = pool

    def test_create(self):

        table = TObjectTable(conn=self.pool, table='tobjects', klass=Record)
        r = table.create(key='books', title='Books', description='A library')
        r = resolve_future(r)
        pprint(r)