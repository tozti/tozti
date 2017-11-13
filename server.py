#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# This file is part of Tozti.

# Tozti is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Tozti.  If not, see <http://www.gnu.org/licenses/>.


import pkg_resources

from aiohttp import web
import logbook
import yaml


__version__ = '0.1'


def main():
    """Entry point for server startup."""

    import sys
    
    # logging stuff
    log_handler = logbook.StreamHandler(sys.stdout)
    log_handler.push_application()

    log = logbook.Logger('tozti')

    # handle configuration
    if len(sys.argv) > 1:
        cfg_file = sys.argv[1]
    else:
        cfg_file = 'config.yml'
    try:
        with open(cfg_file, 'r') as s:
            config = yaml.load(s)
    except FileNotFoundError:
        log.error('could not find config file `{}`'.format(cfg_file))
        sys.exit(1)
    except yaml.YAMLError as e:
        log.error('could not parse config file `{}`: {}'.format(cfg_file, e))
        sys.exit(1)

    app = web.Application(logger=log)
    app['config'] = config

    # module hooks for startup
    for entry in pkg_resources.iter_entry_points(group='tozti', name='register'):
        entry.load()(app)

    # spin up the server
    web.run_app(app, host=config['http']['host'], port=config['http']['port'])


if __name__ == "__main__":
    main()
