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
from pkg_resources import iter_entry_points, resource_string
import sys

from aiohttp import web
import logbook
import yaml
import pystache

from tozti import logger


def create_app(config, mode):
    """Create the main `aiohttp.web.Application` object.

    :param config: path to the yaml config file
    :param mode: string that is either ``dev`` or ``prod``

    It will iterate on every setuptools entrypoint in group ``tozti``
    with name ``manifest`` and add it to the application. See `docs`_.

    .. docs: #FIXME write about creating extensions in the doc.
    """

    app = web.Application()
    app['config'] = config

    # list of things to include to the main index.html
    includes = []

    # load extensions
    for ept in iter_entry_points(group='tozti', name='manifest'):
        logger.info('Loading extension {0.project_name} ({0.location})'
                    .format(ept.dist))
        try:
            manifest = ept.load()
            prefix = ept.dist.project_name
            if 'router' in manifest:
                manifest['router'].add_prefix('/api/{}'.format(prefix))
                app.router.add_routes(manifest['router'])
            if 'includes' in manifest:
                includes.extend('/static/{}/{}'.format(prefix, path)
                                for path in manifest['includes'])
            if '_god_mode' in manifest:
                manifest['_god_mode'](app)
            if mode == 'dev' and 'static_dir' in manifest:
                static_dir = os.path.join(ept.dist.location,
                                          manifest['static_dir'])
                if os.path.isdir(static_dir):
                    app.router.add_static('/static/{}'.format(prefix),
                                          static_dir)
        except Exception as err:
            raise ValueError(
                'Error while loading extension {0.project_name}: {1}'
                .format(ept.dist, err))

    # setup the handler for index.html
    index_html = render_index(includes)
    if mode == 'dev':
        async def handler(req):
            return web.Response(text=index_html, content_type="text/html",
                                charset="utf-8")
        app.router.add_get('/{_:(?!api|static).*}', handler)

        # look at the real location in case some extensions are installed in
        # production mode
        static_dir = os.path.join(sys.prefix, 'share', 'tozti')
        if os.path.isdir(static_dir):
            app.router.add_static('/static', static_dir)
    else:
        path = [sys.prefix, 'share', 'tozti', 'index.html']

        with open(os.path.join(*path), 'w') as s:
            s.write(index_html)

    return app


def render_index(includes):
    """Create the index.html file with the right things included."""

    context = {
        'styles': [{src: u} for u in includes if u.split('.')[-1] == 'css'],
        'scripts': [{src: u} for u in includes if u.split('.')[-1] == 'js']}

    return pystache.render(
        resource_string(__name__, 'templates/index.html'), context)


def main():
    """Entry point for server startup."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config', default='./config.yml',
        help='configuration file (default: `./config.yml`)')
    parser.add_argument('mode', choices=('dev',))  # FIXME: handle `prod` mode
    args = parser.parse_args()

    # FIXME: do config file validation
    logger.debug('Loading configuration'.format(args.config))
    try:
        with open(args.config) as s:
            config = yaml.load(s)
    except Exception as err:
        logger.critical('Error while loading configuration: {}'.format(err))
        sys.exit(1)

    # logging handlers
    # FIXME: make things fancier and configurable (logrotate, etc)
    if args.mode == 'dev':
        handler = logbook.StreamHandler(sys.stdout)
        handler.push_application()

    logger.debug('Initializing app')
    try:
        app = create_app(config, args.mode)
    except Exception as err:
        logger.critical('Error during initialization: {}'.format(err))
        sys.exit(1)

    logger.debug('Setting up asyncio')
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    srv = loop.run_until_complete(loop.create_server(
        handler,
        config['http']['host'],
        config['http']['port']))
    logger.info('Listening on {host}:{port}'.format(**config['http']))

    try:
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
