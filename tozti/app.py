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

# You should have received a copy of the GNU Affero General Public Licensefoo/blo/baz
# along with Tozti.  If not, see <http://www.gnu.org/licenses/>.


__all__ = ('DependencyCycle', 'App')


import asyncio
import os

import logbook
import pystache
from aiohttp import web

import tozti


logger = logbook.Logger('tozti.app')


class DependencyCycle(Exception):
    """Exception raised when a dependency cycle is detected in extensions."""
    pass


class App:
    """The Tozti server."""

    def __init__(self):
        self._app = web.Application()
        self._includes = {}
        self._static_dirs = {}
        self._dep_graph = {}
        self._includes_after = []

    def register(self, prefix, router=None, includes=(), static_dir=None,
                 dependencies=(), _god_mode=None, on_response_prepare=None,
                 on_startup=None, on_cleanup=None, on_shutdown=None,
                 _includes_after=()):
        """Register an extension."""

        logger.info('Registrating extension {}'.format(prefix))

        # some sanity checks
        if static_dir is not None and not os.path.isdir(static_dir):
            raise ValueError('Static directory {} does not exist'.format(
                             static_dir, prefix))
        if len(includes) + len(_includes_after) > 0 and static_dir is None:
            raise ValueError('Includes given but no static directory')
        for inc in includes + _includes_after:
            if not os.path.isfile(os.path.join(static_dir, inc)):
                raise ValueError('Included file {} does not exist in {}, did '
                                 'you execute `npm run build`?'
                                 .format(inc, static_dir))

        # register new api routes
        if router is not None:
            router.add_prefix('/api/{}'.format(prefix))
            self._app.router.add_routes(router)

        # js and static files stuff
        if static_dir is not None:
            self._static_dirs[prefix] = static_dir
        inc_fmt = '/static/{}/{{}}'.format(prefix)
        self._includes[prefix] = [inc_fmt.format(incl) for incl in includes]
        self._dep_graph[prefix] = dependencies
        self._includes_after.extend(inc_fmt.format(incl) for incl in _includes_after)

        # signal handlers
        if on_response_prepare is not None:
            self._app.on_response_prepare.append(on_response_prepare)
        if on_startup is not None:
            self._app.on_startup.append(on_startup)
        if on_cleanup is not None:
            self._app.on_cleanup.append(on_cleanup)
        if on_shutdown is not None:
            self._app.on_shutdown.append(on_shutdown)

        # last-resort hook to do whatever you want
        if _god_mode is not None:
            _god_mode(self._app)

    def _toposort_includes(self):
        """Given includes, a dictionnary of dependencies & includes for each
        extensions, will construct a list of includes file sorted so that
        dependencies are respected.
        """

        visited = set()
        seen_traversal = set()
        def visit(node):
            visited.add(node)
            seen_traversal.add(node)
            for dep in self._dep_graph[node]:
                if dep in seen_traversal:
                    raise DependencyCycle(dep, node)
                if not dep in visited:
                    yield from visit(dep)
            seen_traversal.discard(node)
            yield from self._includes[node]

        for dep in self._dep_graph:
            if not dep in visited:
                yield from visit(dep)

    def _render_index(self):
        logger.debug('Rendering index.html')
        incs = list(self._toposort_includes()) + self._includes_after

        context = {
            'styles': [{'src': u} for u in incs if u.split('.')[-1] == 'css'],
            'scripts': [{'src': u} for u in incs if u.split('.')[-1] == 'js']
        }

        template = os.path.join(tozti.TOZTI_BASE, 'tozti', 'templates',
                                'index.html')
        with open(template) as t:
            return pystache.render(t.read(), context)

    def main(self, production=True, loop=None):
        """Start the server."""

        index_html = self._render_index()

        if production:
            #FIXME: deploy static files and index.html
            pass
        else:
            for (prefix, path) in self._static_dirs.items():
                self._app.router.add_static('/static/{}'.format(prefix), path)
            async def index_handler(req):
                return web.Response(text=index_html, content_type='text/html',
                                    charset='utf-8')
            self._app.router.add_get('/{_:(?!api|static).*}', index_handler)

        for r in self._app.router.resources():
            logger.debug('route: {}'.format(r))

        logger.debug('Setting up asyncio')
        if loop is None:
            loop = asyncio.get_event_loop()

        handler = self._app.make_handler()
        srv = loop.run_until_complete(loop.create_server(
            handler, host=tozti.CONFIG['http']['host'],
            port=tozti.CONFIG['http']['port']))
        logger.info('Listening on {}:{}'.format(tozti.CONFIG['http']['host'],
            tozti.CONFIG['http']['port']))

        try:
            logger.debug('Starting up')
            loop.run_until_complete(self._app.startup())
            logger.info('Finished boot sequence')
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info('Received SIGINT')
        finally:
            logger.info('Initiating shutdown')
            srv.close()
            loop.run_until_complete(srv.wait_closed())
            loop.run_until_complete(self._app.shutdown())
            loop.run_until_complete(handler.shutdown(60.0))
            loop.run_until_complete(self._app.cleanup())
            logger.info('Shutdown complete, goodbye')
        loop.close()
