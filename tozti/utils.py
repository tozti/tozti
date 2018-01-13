# -*- coding:utf-8 -*-

# This file is part of Tozti.

# Tozti is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Tozti is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Tozti.  If not, see <http://www.gnu.org/licenses/>.


from aiohttp.web import json_response as original_json_response
from json import JSONEncoder, dumps
from datetime import datetime
from uuid import UUID

class RouteDef:
    """Definition of a route.

    The method :meth:`get`, :meth:`post`, :meth:`put`, etc can be used as
    decorators to specify the handler for the given HTTP method.
    """

    def __init__(self, path, name=None):
        self._path = path
        self._name = name
        self._routes = {}
        self._prefix = ''

    def register(self, app):
        """Add all our routes to the given `aiohttp.web.Application`."""

        route = app.add_resource(self._path, name=self._name)
        route.add_prefix(self._prefix)
        for m, h in self._routes.items():
            route.add_route(m, h)

    def route(self, *meth):
        """Decorator (with arguments) used to specify HTTP handler."""

        def decorator(handler):
            for m in meth:
                self._routes[m] = handler
            return handler
        return decorator

    def get(self, handler):
        """Decorator used to specify ``GET`` method handler."""

        self._routes['GET'] = handler
        return handler

    def post(self, handler):
        """Decorator used to specify ``GET`` method handler."""

        self._routes['POST'] = handler
        return handler

    def put(self, handler):
        """Decorator used to specify ``PUT`` method handler."""

        self._routes['PUT'] = handler
        return handler

    def patch(self, handler):
        """Decorator used to specify ``PATCH`` method handler."""

        self._routes['PATCH'] = handler
        return handler

    def delete(self, handler):
        """Decorator used to specify ``DELETE`` method handler."""

        self._routes['DELETE'] = handler
        return handler

    def head(self, handler):
        """Decorator used to specify ``HEAD`` method handler."""

        self._routes['HEAD'] = handler
        return handler

    def options(self, handler):
        """Decorator used to specify ``OPTIONS`` method handler."""

        self._routes['OPTIONS'] = handler
        return handler

    def any(self, handler):
        """Decorator used to specify handler for every method."""

        self._routes['*'] = handler
        return handler


class RouterDef:
    """Handle route definitions.

    This object can be used as argument to
    :meth:`aiohttp.web.UrlDispatcher.add_routes`.

    Sample usage::

        router = RouterDef()
        route = router.add_route('/foo')

        @route.get
        def handle_get(req):
            return ...

    See `aiohttp`_ for more informations on resources and routing.

    .. _aiohttp: https://aiohttp.readthedocs.io/en/stable/web.html#resources-and-routes
    """

    def __init__(self):
        self._routes = []

    def add_route(self, path, name=None):
        """Add and return a route with given path to the router."""

        r = RouteDef(path, name=name)
        self._routes.append(r)
        return r

    def add_prefix(self, prefix):
        """Prefix every contained route."""

        for r in self._routes:
            r._prefix = prefix

    def __iter__(self):
        return iter(self._routes)


API_ERRORS = {}

def register_error(name, fmt, status):
    if name in API_ERRORS:
        raise ValueError('error %s already defined' % name)
    API_ERRORS[name] = (len(API_ERRORS), fmt, status)

def api_error(name, **vars):
    code, fmt, status = API_ERRORS[name]
    return json_response({'error': code, 'msg': fmt.format(**vars)},
                         status=status)

def json_response(data, **kwargs):
    fancy_dumps = lambda obj: dumps(obj, cls=ExtendedJSONEncoder)
    return original_json_response(data, dumps=fancy_dumps, **kwargs)

class ExtendedJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return str(obj)
        else:
            super().default(obj)