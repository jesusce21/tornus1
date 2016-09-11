# -*- coding: utf-8 -*-
"""
(C) 2016 Ángel Olea Gómez   www.ovalo-software.com

Definición de los TObject que forman la aplicación Record, Field y Action

---------------- ------------------------------------------
2016-09-10 05:09 - aolea - creation

"""
from tornus1.tobject import TObject, AttrString


class Base(TObject):

    title = AttrString(required=True)
    description = AttrString()


class Record(Base):
    pass

#     fields = AttrComposition(Field)
#     actions = AttrComposition(Action)
#
#
# class Field(Base):
#
#     parent_id = AttrParent(Record)
#     field_type = AttrInclusion(required=True, enum=(('string', FieldString),
#                                                      'integer'))
#
#
# class Action(Base):
#
#     parent_id = AttrParent(Record)
#     initial_status = AttrString()
#     action_type = AttrString(required=True, enum=['form'])
#     final_status = AttrString()
#
#
# class FieldString(TComponent):
#
#     max_length = AttrInteger()
