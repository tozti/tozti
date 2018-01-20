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


__all__ = ('DependencyCycle', 'App', 'Extension')


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


class Extension:
    """A tozti extension

    Represents a Tozti extension

    Attributes:
        name (str): The name of the extension
        includes (list): A list of files included by the extension
        static_dir (str): Path of the static dir of the module
        _god_mode (function): `god mode` function
        on_response_prepare (function): A function to be executed when the hook\
            on_response_prepare is executed by aiohttp
        on_cleanup (function): A function to be executed when the hook\
            on_cleanup is executed by aiohttp
        on_startup (function): A function to be executed when the hook\
            on_response_prepare is executed by aiohttp
        on_shutdown (function): A function to be executed when the hook\
            on_shutdown is executed by aiohttp
        includes_after (list): list of files that must be included after every modules\
            have included their files. Note, this shouldn't be defined my extensions directly

    """
    def __init__(self, name, router=None, includes=(), static_dir=None,
                 dependencies=(), _god_mode=None, on_response_prepare=None,
                 on_startup=None, on_cleanup=None, on_shutdown=None,
                 **kwargs):
        """ Build an extension from a list of its attributes (a MANIFEST for example).
        (TODO) Put a warning if an attribute which is not necessary in an extension is 
            passed as argument.
        """

        self.name = name

        self.router = router
        self.includes = includes if isinstance(includes, list) else list(includes) 
        self.static_dir = static_dir
        self.dependencies = set(dependencies)
        self._god_mode = _god_mode
        self.on_response_prepare = on_response_prepare
        self.on_startup = on_startup
        self.on_cleanup = on_cleanup
        self.on_shutdown = on_shutdown
        self.includes_after = []

        if len(kwargs) > 0:
            # TODO do something here. If kwargs is not empty, that means the manifest 
            # contain an entry wich is not well defined
            pass

    def set_static_dir_absolute(self, absolute_prefix):
        """
        Set this extension static dir to be absolute.
        Check if this is feasible

        Args:
            absolute_prefix: the absolute path that will lead to static_path after transformation
        """
        # TODO check if the static dir isn't already absolute
        # this is a function only so that writing tests is feasible
        self.static_dir = os.path.join(absolute_prefix, self.static_dir)

    def check_sane(self):
        """Check if the extension is sane.
        In other words, check if the every files it refers to exists

        Raises:
            ValueError exception if one check failed.
        """
        if self.static_dir is not None and not os.path.isdir(self.static_dir):
            raise ValueError('Static directory {} does not exist'.format(
                             self.static_dir, self.name))
        if len(self.includes) + len(self.includes_after) > 0 and self.static_dir is None:
            raise ValueError('Includes given but no static directory')
        for inc in self.includes + self.includes_after:
            if not os.path.isfile(os.path.join(self.static_dir, inc)):
                raise ValueError('Included file {} does not exist in {}, did '
                                 'you execute `npm run build`?'
                                 .format(inc, self.static_dir))

    def add_prefix_routes(self, prefix, append_name=True):
        if append_name:
            prefix = "{}/{}".format(prefix, self.name)
        self.router.add_prefix(prefix)


class DependencyGraph:
    """Represents a dependency graph

    Tozti uses this to compute an order in which extensions are to be included so 
    that extensions depending on other extensions are included after their
    dependencies
    """

    def __init__(self):
        self._node_value = {}
        self._dependencies = {}

    def add_node(self, name, dependencies, value):
        """Add a node with its value and dependencies to the graph

        Args:
            name: the identifier of the new node
            dependencies(iterable): The list of the id's of nodes on whom
                the new node depends
            value: the value of this node
        """
        self._dependencies[name] = dependencies
        self._node_value[name] = value

    def toposort(self):
        """Compute a topological sort on the graph

        Yields:
            list: a list of node's values in topological order 
        """
        visited = set()
        seen_traversal = set()
        def visit(node):
            visited.add(node)
            seen_traversal.add(node)
            for dep in self._dependencies[node]:
                if dep in seen_traversal:
                    raise DependencyCycle(dep, node)
                if not dep in visited:
                    yield from visit(dep)
            seen_traversal.discard(node)
            yield from self._node_value[node]

        for dep in self._dependencies:
            if not dep in visited:
                yield from visit(dep)


class App:
    """The Tozti server."""

    def __init__(self):
        self._app = web.Application()
        self._static_dirs = {}
        self._includes_after = []
        self._dep_graph_includes = DependencyGraph()

    def register(self, extension):
        """Register an extension."""

        logger.info('Registrating extension {}'.format(extension.name))

        # some sanity checks
        # probably check for exceptions here
        extension.check_sane()

        # register new api routes
        if extension.router is not None:
            extension.add_prefix_routes("/api")
            self._app.router.add_routes(extension.router)

        # js and static files stuff
        # TODO refactor
        if extension.static_dir is not None:
            self._static_dirs[extension.name] = extension.static_dir

        
        inc_fmt = '/static/{}/{{}}'.format(extension.name)
        self._dep_graph_includes.add_node(extension.name,extension.dependencies, 
                                              [inc_fmt.format(incl) for incl in extension.includes])
        self._includes_after.extend(inc_fmt.format(incl) for incl in extension.includes_after)

        # signal handlers
        if extension.on_response_prepare is not None:
            self._app.on_response_prepare.append(extension.on_response_prepare)
        if extension.on_startup is not None:
            self._app.on_startup.append(extension.on_startup)
        if extension.on_cleanup is not None:
            self._app.on_cleanup.append(extension.on_cleanup)
        if extension.on_shutdown is not None:
            self._app.on_shutdown.append(extension.on_shutdown)

        # last-resort hook to do whatever you want
        if extension._god_mode is not None:
            extension._god_mode(self._app)


    def _render_index(self):
        logger.debug('Rendering index.html')
        incs = list(self._dep_graph_includes.toposort()) + self._includes_after

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

        self._app['tozti-config'] = tozti.CONFIG

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
