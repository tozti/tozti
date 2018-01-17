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


import argparse
from importlib.util import spec_from_file_location, module_from_spec
import os
import sys

import logbook
import toml

import tozti
import tozti.store
import tozti.app


logger = logbook.Logger('tozti.main')


def find_exts():
    """Register the extensions found.

    Returns the list of includes and the list of static directories. See
    the `docs`_ for the manifest format.

    .. docs: https://tozti.readthedocs.io/en/latest/dev/arch.html#extensions
    """

    includes = {}
    deps = {}
    static_dirs = []

    for ext in os.listdir(os.path.join(tozti.TOZTI_BASE, 'extensions')):
        extpath = os.path.join(tozti.TOZTI_BASE, 'extensions', ext)
        if not os.path.isdir(extpath):
            continue

        logger.info('Loading extension {}'.format(ext))

        mod_path = os.path.join(extpath, 'server.py')
        pkg_path = os.path.join(extpath, 'server', '__init__.py')
        if os.path.isfile(mod_path):
            spec = spec_from_file_location(ext, mod_path)
        elif os.path.isfile(pkg_path):
            spec = spec_from_file_location(ext, pkg_path)
        else:
            msg = 'Could not find python file for extension {}'
            raise ValueError(msg.format(ext))

        mod = module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as err:
            msg = 'Error while loading extension {}, skipping: {}'
            logger.exception(msg.format(ext, err))
            continue

        try:
            #FIXME: validate the manifest format
            yield (ext, mod.MANIFEST)
        except AttributeError:
            logger.exception('Error while loading extension {}, skipping: no '
                             'MANIFEST found'.format(ext))
            continue


def main():
    """Entry point for server startup."""

    parser = argparse.ArgumentParser('tozti')
    parser.add_argument(
        '-c', '--config', default=os.path.join(tozti.TOZTI_BASE, 'config.toml'),
        help='configuration file (default: `TOZTI/config.toml`)')
    parser.add_argument('command', choices=('dev',))  # FIXME: handle `prod` mode
    args = parser.parse_args()

    # logging handlers
    # FIXME: make things fancier and configurable (logrotate, etc)
    logbook.compat.redirect_logging()
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
    tozti.CONFIG = config


    # initialize app
    logger.debug('Initializing app')
    app = tozti.app.App()

    # load and register extensions
    try:
        for (prefix, man) in find_exts():
            # add dependency on the core
            if 'dependencies' in man and 'core' not in man['dependencies']:
                man['dependencies'].append('core')
            else:
                man['dependencies'] = ['core']
            # make static_dir absolute and default to 'dist'
            if 'static_dir' not in man:
                man['static_dir'] = 'dist'
            man['static_dir'] = os.path.join(tozti.TOZTI_BASE, 'extensions',
                prefix, man['static_dir'])
            app.register(prefix, **man)
    except Exception as err:
        logger.critical('Error while loading extensions {}: {}'.format(prefix, err))
        sys.exit(1)

    # register core api
    try:
        app.register('store', router=tozti.store.router,
                     on_startup=tozti.store.open_db,
                     on_shutdown=tozti.store.close_db)
        app.register('core', static_dir=os.path.join(tozti.TOZTI_BASE, 'dist'),
                     includes=['bootstrap.js'], _includes_after=['launch.js'])
    except Exception as err:
        logger.critical('Error while loading core: {}'.format(err))
        sys.exit(1)

    try:
        app.main(production=args.command=='prod')
    except tozti.app.DependencyCycle as err:
        logger.critical('Found dependency cycle between extensions {} and {}'
                        .format(err.args[0], err.args[1]))

main()
