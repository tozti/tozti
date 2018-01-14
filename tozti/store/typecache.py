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


from collections import namedtuple
import re

import jsonschema
import aiohttp
from jsonschema.exceptions import ValidationError

from tozti.store import UUID_RE


META_SCHEMA = {
    'type': 'object',
    'properties': {
        'attributes': {
            'type': 'object',
            'patternProperties': {
                '.*': jsonschema.Draft4Validator.META_SCHEMA,
            }
        },
        'relationships': {
            'type': 'object',
            'patternProperties': {
                '.*': {
                    'anyOf': [{
                        'type': 'object',
                        'properties': {
                            'reverse-of': {
                                'type': 'object',
                                'properties': {
                                    'type': { 'type': 'string', 'format': 'uri' },
                                    'path': { 'type': 'string' },
                                },
                                'required': ['type', 'path'],
                            },
                        },
                        'required': ['reverse-of']
                    }, {
                        'type': 'object',
                        'properties': {
                            'arity': {
                                'type': 'string',
                                'pattern': '^(to-one|to-many)$',
                            },
                            'type': { 'type': 'string', 'format': 'uri' }
                        },
                        'required': ['arity'],
                    }]
                }
            }
        }
    },
    'additionalProperties': False,
    'required': ['attributes', 'relationships'],
}


Schema = namedtuple('Schema', ('attrs', 'to_one', 'to_many', 'autos'))


class TypeCache:
    def __init__(self):
        self._cache = {}

    def compile_schema(self, raw, name):
        attrs = raw['attributes']

        to_one = {}
        to_many = {}
        autos = {}
        for (rel, rel_def) in raw['relationships'].items():
            if 'reverse-of' in rel_def:
                autos[rel] = (rel_def['reverse-of']['type'],
                              rel_def['reverse-of']['path'])
                continue

            if 'type' in rel_def:
                if isinstance(rel_def['type'], str):
                    pat = '^%s$' % re.escape(rel_def['type'])
                else:
                    pat = '^(%s)$' % '|'.join(map(re.escape, rel_def['type']))
                type_s = {'type': 'string',
                          'format': 'uri',
                          'pattern': pat}
            else:
                type_s = {'type': 'string', 'format': 'uri'}
            data_s = {'type': 'object',
                      'properties': {'id': {'type': 'string',
                                            'pattern': '^%s$' % UUID_RE},
                                     'type': type_s},
                      'required': ['id']}

            if rel_def['arity'] == 'to-one':
                to_one[rel] = {'type': 'object', 'properties': {'data': data_s}}
            elif rel_def['arity'] == 'to-many':
                to_many[rel] = {'type': 'object',
                                'properties': {'data': {'type': 'array',
                                                        'items': data_s}},
                                'required': ['data']}
            else:
                raise AssertionError('BAD! Invalid schema after validation')

        return Schema(attrs, to_one, to_many, autos)

    async def __getitem__(self, type_url):
        if type_url in self._cache:
            return self._cache[type_url]

        print(type_url)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(type_url) as resp:
                    assert resp.status == 200
                    raw_schema = await resp.json()
        except ValueError as err:
            print(type(err))
            raise ValueError('error while retrieving type schema: {}'.format(err))

        try:
            jsonschema.validate(raw_schema, META_SCHEMA)
        except ValidationError as err:
            raise ValueError('invalid schema: %s' % err.message)

        schema = self.compile_schema(raw_schema, type_url)
        self._cache[type_url] = schema
        return schema
