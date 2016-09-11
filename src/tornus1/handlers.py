# -*- coding: utf-8 -*-
"""
(C) 2016 Ángel Olea Gómez   www.ovalo-software.com

#FIXME description

---------------- ------------------------------------------
2016-09-10 15:11 - aolea - creation

"""
import os
import tornado
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.gen import coroutine

import mako
import mako.template
import mako.lookup

from pyjade.ext.mako import preprocessor as mako_preprocessor


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.lookup_templates = mako.lookup.TemplateLookup([application.settings['template_path']],
                                                           preprocessor=mako_preprocessor,
                                                           input_encoding='utf-8',
                                                           output_encoding='utf-8')

    def render(self, template_name, **data):
        tem = self.lookup_templates.get_template(template_name)
        # TODO: i18n
        data['_'] = lambda x: x
        self.finish(tem.render(**data))

    def get_input(self):
        input_ = {cmp: tornado.escape.xhtml_escape(self.get_argument(cmp)) for cmp in
                  self.request.arguments}
        return input_


class RootHandler(BaseHandler):
    pass


class TObjectHandler(BaseHandler):

    def initialize(self, table, views):
        self.table = table
        self.views = views

    @coroutine
    def get(self, path):
        """
        GET:
        ----
        list
        new
        <id>/edit
        <id>/show

        :param path:
        :return:
        """
        slices = [i for i in path.split('/') if i]

        if len(slices) == 0:
            self._list()

        else:
            verb = slices[-1]

            if verb == 'list':

                self._list()

            elif verb == 'new':

                self._new()

            elif verb == 'show':

                if len(slices) < 2:
                    raise tornado.web.HTTPError(404)
                self._show(slices[1])

            elif verb == 'edit':

                if len(slices) < 2:
                    raise tornado.web.HTTPError(404)
                self._edit(slices[1])

    @coroutine
    def _render_response(self, verb, data):
        # TODO: json
        self.render(os.path.join(self.views, verb+'.jade'), **data)

    @coroutine
    def _list(self):
        # data = yield self.table.list(self.get_input())
        data = {}
        self._render_response('list', data)

    @coroutine
    def _new(self):
        data = yield self.table.new()
        self._render_response('new', data)

    @coroutine
    def _read(self, key):
        data = yield self.table.read(key)
        if not data:
            raise tornado.web.HTTPError(404)
        return data

    @coroutine
    def _show(self, key):
        data = yield self._read(key)
        self._render_response('show', data)

    @coroutine
    def _edit(self, key):
        data = yield self._read(key)
        self._render_response('edit', data)

    @coroutine
    def post(self, path):
        """
        POST:
        ----
        create
        <id>/update
        <id>/delete
        <id>/move

        fields/create
        fields/<id>/update
        fields/<id>/delete
        fields/<id>/move

        :param path:
        :return:
        """
        slices = path.split('/')

        if len(slices) == 0 or slices[0] in ('create', 'new'):

            self._create()

    def _create(self):

        data = yield self.klass(self.context, self.get_input()).create()
        if data.status:
            self.redirect('yoquese')
        else:
            self._render_response('new', data)





