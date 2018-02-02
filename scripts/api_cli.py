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
    ans = resp.json()
    if len(resp.cookies)>0:
        print('Cookie(s) : ', requests.utils.dict_from_cookiejar(resp.cookies))
    if 'errors' not in ans:
        return ans
    print('ERROR: %s (status: %s)' % (ans['errors'][0]['code'], resp.status_code))
    print(ans['errors'][0]['detail'])

def create_resource(**kwargs):
    ans = check_call('post', '/store/resources', json={'data': kwargs})
    if ans is not None:
        pprint(ans['data'])
        return ans['data']['id']


def get_resource(id):
    ans = check_call('get', '/store/resources/%s' % id)
    if ans is not None:
        return ans['data']


def update_resource(id, **kwargs):
    ans = check_call('patch', '/store/resources/%s' % id,
                             json={'data': kwargs})
    if ans is not None:
        pprint(ans['data'])


def delete_resource(id):
    check_call('delete', '/store/resources/%s' % id)
    
