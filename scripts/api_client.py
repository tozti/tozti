# -*- coding: utf-8 -*-

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


import requests
from requests import get, post, put, patch, delete
from pprint import pprint


API = 'http://127.0.0.1:8080/api'


class APIError(Exception):
    def __init__(self, code, **kwargs):
        super().__init__(code, kwargs.values())
        self.code = code
        self.status = kwargs.get('status')
        self.detail = kwargs.get('detail')
        self.traceback = kwargs.get('traceback')

    def __str__(self):
        msg = self.code
        if self.status is not None:
            msg += ' [%s]' % self.status
        if self.detail is not None:
            msg += ': %s' % self.detail
        if self.traceback is not None:
            msg += '\n=== SERVER TRACEBACK ===\n%s' % self.traceback
        return msg


def check_call(meth, path, json=None, prefix=API):
    """Make an API call.

    Raises APIError in case the api returns an error. Raises JSONDecodeError
    if the response is not valid JSON.
    """

    resp = requests.request(meth, prefix + path, json=json)
    ans = resp.json()
    if 'errors' in ans:
        raise APIError(**ans['errors'][0])
    return ans


## Resource endpoints

def resource_create(**kwargs):
    """Create and return a resource.

    You should pass `type`, `attributes` and optionally `relationships` as
    arguments.
    """

    ans = check_call('POST', '/store/resources', json={'data': kwargs})
    return ans['data']


def resource_fetch(id):
    """Get a resource object by it's UUID."""

    ans = check_call('GET', '/store/resources/%s' % id)
    return ans['data']


def resource_update(id, **kwargs):
    """Partially update a resource.

    You can only change attributes and relationships.
    """

    ans = check_call('PATCH', '/store/resources/%s' % id,
                             json={'data': kwargs})
    return ans['data']


def resource_delete(id):
    """Delete a resource by it's UUID."""

    check_call('DELETE', '/store/resources/%s' % id)


## Relationship endpoints

def relationship_get(id, rel):
    """Get a relationship."""

    return check_call('GET', '/store/resources/%s/%s' % (id, rel))


def relationship_update(id, rel, data):
    """Overwrite a relationship."""

    return check_call('PUT', '/store/resources/%s/%s' % (id, rel),
                      json={'data': data})


def relationship_append(id, rel, *data):
    """Append items to a to-many relationship."""

    return check_call('POST', '/store/resources/%s/%s' % (id, rel),
                      json={'data': data})


def relationship_delete(id, rel, *data):
    """Delete items from a to-many relationship."""

    return check_call('DELETE', '/store/resources/%s/%s' % (id, rel),
                      json={'data': data})
