# -*- coding: utf-8 -*-
"""
(C) 2016 Ángel Olea Gómez   www.ovalo-software.com

Test de Tobject

---------------- ------------------------------------------
2016-09-11 15:39 - aolea - creation

"""
from pprint import pprint
import unittest

from tornus1.tobject import TObject, AttrString, TContext, TComponent


class TObjectTestCase(unittest.TestCase):

    def test_component(self):

        class TTest(TComponent):

            charfied = AttrString(required=True)

        t = TTest()
        pprint(t.klass)
        t.charfied = 'hh'
        pprint(t)