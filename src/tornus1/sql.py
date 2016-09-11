# -*- coding: utf-8 -*-
"""
(C) 2016 Ángel Olea Gómez   www.ovalo-software.com

Clases que tratan con SQL

---------------- ------------------------------------------
2016-09-09 14:14 - aolea - creation

"""
import re
from tornus1.concurrent import coroutine


class SqlTable:

    def __init__(self, conn, table_name):
        self.conn = conn
        self.table_name = table_name

    @coroutine
    def execute(self, sql, **params):
        cursor = yield self.conn.execute(sql, params)
        result = {'message': cursor.statusmessage}
        if cursor.description:
            result['rows'] = cursor.fetchall()
        return result

    @coroutine
    def begin(self):
        yield self.execute('BEGIN;')

    @coroutine
    def commit(self):
        yield self.execute('COMMIT;')

    @coroutine
    def rollback(self):
        yield self.execute('ROLLBACK;')

    @coroutine
    def select(self, where=None, columns=None, orderby=None, limit=None, page=None):
        sql = sql_select(self.table_name, where, columns, orderby, limit, page)
        r = yield self.execute(sql)
        return r

    @coroutine
    def exists(self, _operator_='and', **conditions):
        pass

    @coroutine
    def count(self, _operator_='and', **conditions):
        pass

    @coroutine
    def read(self, primary_key, exception=False):
        pass

    @coroutine
    def insert(self, **values):
        sql, params = sql_insert(self.table_name, **values)
        r = yield self.execute(sql, **params)
        return r

    @coroutine
    def update(self, primary_key, **values):
        sql, params = sql_update(self.table_name, **values)
        r = yield self.execute(sql, **params)
        return r

    @coroutine
    def delete(self, primary_key):
        pass


class SqlDdlTable:

    @classmethod
    def create(cls, conn, table_name, columns):
        pass

    def __init__(self, conn, table_name):
        self.conn = conn

    def add_colum(self, column):
        pass

    def alter_column(self, column):
        pass


def sanitize(value):
    if not isinstance(value, str) or not re.match(r'[a-zA-Z0-9_]*', value) or len(value) > 64:
        raise ValueError('% is not a valid column or table name' % value)
    return value


def sql_where(columns, operator=' and '):
    """
    :param columns: iterator for column names
    :param operator:
    :return: 'col1=%(col1)s ...'
    """
    where = []
    for column in columns:
        column = sanitize(column)
        where.append('%s=%%(%s)s' % (column, column))
    return operator.join(where)


def sql_select_exists(table, columns):
    """

    :param table:
    :param columns:
    :return:
    """
    table = sanitize(table)
    where = sql_where(columns)
    sql = 'select exists(select 1 from %s where %s)' % (table, where)
    return sql


def sql_select(table, where=None, columns=None, orderby=None, limit=None, page=None):
    """
    :param table:
    :param where:
    :param columns:
    :param orderby:
    :param limit:
    :param page:
    :return:
    """
    def _to_int(n):
        try:
            n = int(n)
        except TypeError:
            n = None
        return n
    limit = _to_int(limit)
    page = _to_int(page)
    table = sanitize(table)
    columns = columns or '*'
    where = 'where %s' % where if where else ''
    orderby = 'order by %s' % orderby if orderby else ''
    limit_str = 'limit %s' % limit if limit else ''
    offset = 'offset %s' % str((page-1)*limit) if (page and limit) else ''
    sql = 'select %s from %s %s %s %s %s' % (columns, table, where, orderby, limit_str, offset)
    return sql


def sql_insert(table, **values):
    """
    :param table:
    :param values:
    :return:
    """
    table = sanitize(table)
    columns = []
    variables = []
    for col in values.keys():
        col = sanitize(col)
        columns.append(col)
        variables.append('%%(%s)s' % col)
    sql = 'insert into %s (%s) values (%s) ' \
          'returning *' % (table, ','.join(columns), ','.join(variables))
    return sql, values


def sql_update(table, pkcolumns, **values):
    """

    :param table:
    :param values:
    :param pkcolumns:
    :return:
    """
    table = sanitize(table)
    asign = []
    where = []
    for name, value in values.items():
        if name not in pkcolumns:
            asign.append(name + '=%(' + name + ')s')
        else:
            where.append(name + '=%(' + name + ')s')
    sql = 'update %s set %s where %s returning *' % (table, ','.join(asign), ' and '.join(where))
    return sql, values


def sql_delete(table, columns, operator=' and '):
    """
    :param table:
    :param columns:
    :param operator:
    :return:
    """
    table = sanitize(table)
    where = sql_where(columns, operator)
    sql = 'delete from %s where %s' % (table, where)
    return sql


def ddl_list_table_names():
    """
    http://stackoverflow.com/questions/769683/show-tables-in-postgresql
    :return:
    """
    sql = """
        SELECT
            table_name
        FROM
            information_schema.tables
        WHERE
            table_type = 'BASE TABLE'
        AND
            table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY
            table_name;
    """
    return sql
