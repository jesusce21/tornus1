# -*- coding: utf-8 -*-
"""
(C) 2016 Ángel Olea Gómez   www.ovalo-software.com

Modelo TObject que describe y persiste objetos estructurados

---------------- ------------------------------------------
2016-09-09 17:36 - aolea - creation

"""
import simplejson as json
from tornus1.concurrent import coroutine

from tornus1 import sql


class Attr:
    """
    Un Attr es un descriptor para usar en las clases TObject
    """
    def __init__(self, default=None, required=False):
        self.name = None
        self.default = default

    def __get__(self, obj, type=None):
        return obj.get(self.name, self.default)

    def __set__(self, obj, value):
        obj._values[self.name] = value

    def __delete__(self, obj):
        raise ValueError

    def validate(self, obj):
        return None


class AttrString(Attr):
    pass


class WithAttrs(type):
    """
    MetaClass que añade a nivel de clase .attrs con los attrs de type Attr
    """
    def __new__(mcs, name, bases, all_attrs):
        r = super().__new__(mcs, name, bases, all_attrs)

        attrs = {}
        for base in bases:
            at = getattr(base, 'attrs', None)
            if at:
                attrs.update(at)
        for name, value in all_attrs.items():
            if isinstance(value, Attr):
                attrs[name] = value
                value.name = name
        r.attrs = attrs

        return r


class TComponent(metaclass=WithAttrs):

    def __init__(self, **values):
        self._values = {k: v for k, v in values.items() if self.is_attr(k)}

    def is_attr(self, name):
        return name in self.attrs

    @property
    def klass(self):
        return self.__class__.__name__

    def get(self, attr_name, default=None):
        return self._values.get(attr_name, default)

    def validate(self):
        errors = {}
        for attr in self.attrs.values():
            err = attr.validate(self)
            if err:
                errors[attr] = err
        return errors

    def for_json(self):
        return self._values

    def __repr__(self):
        return '%s(%s)' % (self.klass,
                           ', '.join(['%s=%s' % (k, v) for k, v in self._values.items()]))


class TContext:

    def __init__(self, conn):
        self.conn = conn


class TObject(TComponent):

    key = AttrString(required=True)

    parent_id = AttrString()

    @coroutine
    def on_create(self, result):
        return result

    @coroutine
    def on_update(self, result):
        return result


class TObjectTable:
    """
    CREATE TABLE tobjects
    (
      id serial NOT NULL,
      parent_id integer,
      parent_order integer,
      key character varying(64) NOT NULL,
      klass character varying(64) NOT NULL,
      data json NOT NULL,
      CONSTRAINT tobjects_pkey PRIMARY KEY (id)
    );

    ALTER TABLE tobjects ADD CONSTRAINT fk_tobjects_parent FOREIGN KEY (parent_id)
      REFERENCES tobjects(id);
    CREATE UNIQUE INDEX idx_tobjects_parent_key ON tobjects(parent_id, key);
    CREATE INDEX idx_tobjects_key ON tobjects(key);
    CREATE INDEX idx_tobjects_klass ON tobjects(klass);

    """

    def __init__(self, conn, table, klass):
        self.table = sql.SqlTable(conn, table)
        self.klass = klass

    def new(self):
        return self.klass()

    @coroutine
    def create(self, **data):
        tobj = self.klass(**data)
        errors = tobj.validate()
        if errors:
            return errors
        yield self.table.begin()
        r = yield self.table.insert(parent_id=tobj.parent_id, klass=tobj.klass, key=tobj.key,
                                    data=json.dumps(tobj, for_json=True))
        r = yield tobj.on_create(r)
        yield self.table.commit()
        return r

    def list(self, limit=50, offset=None):
        pass

    def read(self, key):
        pass

    def update(self, key, change):
        pass

    def delete(self, key):
        pass


# class TObject(TComponent):
#
#     def __init__(self, context, **values):
#         pass
#
#     @classmethod
#     def list(cls):
#         pass
#
#     @classmethod
#     def new(cls):
#         pass
#
#     @classmethod
#     def read(cls, key):
#         pass
#
#     @coroutine
#     def validate(self):
#         pass
#
#     @coroutine
#     def create(self):
#         pass
#
#     @coroutine
#     def update(self, changes):
#         pass
#
#     @coroutine
#     def delete(self):
#         pass
#
#     @@property
#     def key(self):
#         return
#
#     @@property
#     def klass(self):
#         return
#
#     @@property
#     def parent_id(self):
#         return
#
#     def on_create(self):
#         pass
#
#     def on_update(self):
#         pass
#
#
