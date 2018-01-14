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


def check_call(meth, path, json=None):
    resp = requests.request(meth, API + path, json=json)
    try:
        ans = resp.json()
    except Exception:
        print('ERROR: something went wrong, response was:')
        print(resp.text)
        print()
        return
    if 'error' in ans or resp.status_code != 200:
        print('ERROR: %s (status: %s)' % (ans['error']['code'], resp.status_code))
        print(ans['error']['msg'])
        print()
        return
    return ans

def create_resource(**kwargs):
    resource = check_call('post', '/store/resources', json=kwargs)['data']
    pprint(resource)
    print()
    return resource['id']


def get_resource(id):
    return check_call('get', '/store/resources/%s' % id)['data']


def delete_resource(id):
    check_call('delete', '/store/resources/%s' % id)
