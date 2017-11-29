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


import argparse
import asyncio
import os.path
import sys

from aiohttp import web
import logbook
import pystache
from pkg_resources import iter_entry_points, resource_string
import toml

from tozti import logger


def load_exts(app):
    """Search and register the extensions.

    Returns the list of paths to include and the list of static directories.

    Iterate on every setuptools entrypoint in group ``tozti`` with name
    ``manifest`` and add it to the application. See the `docs`_ for the
    manifest format.

    .. docs: https://tozti.readthedocs.io/en/latest/dev/arch.html#extensions
    """

    includes = []
    static_dirs = []

    for ept in iter_entry_points(group='tozti', name='manifest'):
        logger.info('Loading extension {0.project_name} ({0.location})'
                    .format(ept.dist))
        try:
            manifest = ept.load()
            prefix = manifest['name']
            if 'router' in manifest:
                manifest['router'].add_prefix('/api/{}'.format(prefix))
                app.router.add_routes(manifest['router'])
            if '_god_mode' in manifest:
                manifest['_god_mode'](app)
            if 'includes' in manifest:
                includes.extend('/static/{}/{}'.format(prefix, inc)
                                for inc in manifest['includes'])
            static_dirs.append((prefix, os.path.join(ept.dist.location, 'dist')))
        except Exception as err:
            raise ValueError(
                'Error while loading extension {0.project_name}: {1}'
                .format(ept.dist, err))

    return (includes, static_dirs)


def render_index(includes):
    """Create the index.html file with the right things included."""

    context = {
        'styles': [{'src': u} for u in includes if u.split('.')[-1] == 'css'],
        'scripts': [{'src': u} for u in includes if u.split('.')[-1] == 'js']
    }

    return pystache.render(resource_string(__name__, 'templates/index.html'),
                           context)


def main():
    """Entry point for server startup."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config', default='./config.toml',
        help='configuration file (default: `./config.toml`)')
    parser.add_argument('command', choices=('dev',))  # FIXME: handle `prod` mode
    args = parser.parse_args()

    # logging handlers
    # FIXME: make things fancier and configurable (logrotate, etc)
    if args.command == 'dev':
        handler = logbook.StreamHandler(sys.stdout)
        handler.push_application()

    # config file
    # FIXME: do config file validation
    logger.debug('Loading configuration'.format(args.config))
    try:
        with open(args.config) as s:
            config = toml.load(s)
    except Exception as err:
        logger.critical('Error while loading configuration: {}'.format(err))
        sys.exit(1)

    # initialize app
    logger.debug('Initializing app')
    app = web.Application()
    app['config'] = config
    try:
        includes, statics = load_exts(app)
    except Exception as err:
        logger.critical('Error during initialization: {}'.format(err))
        sys.exit(1)

    # deploy static files
    if args.command == 'dev':
        for (name, dir) in statics:
            app.router.add_static('/static/{}'.format(name), dir)

    # render index.html
    logger.debug('Rendering index.html')
    index_html = render_index(includes)
    if args.command == 'dev':
        async def index_handler(req):
            return web.Response(text=index_html, content_type="text/html",
                                charset="utf-8")
        app.router.add_get('/{_:(?!api|static).*}', index_handler)

    logger.debug('Setting up asyncio')
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    srv = loop.run_until_complete(loop.create_server(
        handler,
        config['http']['host'],
        config['http']['port']))
    logger.info('Listening on {host}:{port}'.format(**config['http']))

    try:
        loop.run_until_complete(app.startup())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Received SIGINT, initiating shutdown')
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.shutdown())
        loop.run_until_complete(handler.shutdown(60.0))
        loop.run_until_complete(app.cleanup())
        logger.info('Shutdown complete, goodbye')
    loop.close()


main()
