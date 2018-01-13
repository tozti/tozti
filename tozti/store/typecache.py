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

import jsonschema
import aiohttp


Schema = namedtuple('Schema', ('attributes', 'to_one', 'to_many', 'auto',
                               'allowed_rels'))


META_SCHEMA = {
    'type': 'object',
    'properties': {
        'attributes': jsonschema.Draft4Validator.META_SCHEMA,
        'relationship': {
            'type': 'object',
            'patternProperties': {
                '.*': {
                    'oneOf': [{
                        'type': 'object',
                        'properties': {
                            'reverse-of': {
                                'type': 'object',
                                'properties': {
                                    'type': { 'anyOf': [
                                        { 'type': 'string', 'format': 'uri' },
                                        { 'type': 'string', 'pattern': '^\*$'},
                                     ]},
                                    'path': { 'type': 'string' },
                                }
                            },
                        }
                    }, {
                        'type': 'object',
                        'properties': {
                            'arity': { 'anyOf': [
                                { 'type': 'string', 'pattern': '^to-one$' },
                                { 'type': 'string', 'pattern': '^to-many$' },
                            ]},
                            'target': { 'type': 'string', 'format': 'uri' }
                        }
                    }]
                }
            }
        }
    },
    'additionalProperties': False,
    'required': ['attributes', 'relationships'],
}


class TypeCache:
    def __init__(self):
        self._cache = {}

    async def __getitem__(self, type_url):
        if type_url in self._cache:
            return self._cache[type_url]

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(type_url) as resp:
                    assert resp.status == 200
                    raw_schema = await resp.json()
        except:
            raise ValueError('error while retrieving type schema')

        try:
            jsonschema.validate(raw_schema, META_SCHEMA)
        except ValidationError as err:
            raise ValueError('invalid schema: %s' % err.message)

        to_one = []
        to_many = []
        auto = []
        allowed = set()
        for (rel, val) in raw_schema['relationships'].items():
            if 'reverse-of' in val:
                auto.append((rel, val['reverse-of']))
            elif val['arity'] == 'to-one':
                to_one.append((rel, val['target']))
                allowed.add(rel)
            elif val['arity'] == 'to-many':
                to_many.append((rel, val['target']))
                allowed.add(rel)
            else:
                raise AssertionError('?! invalid schema after validation')

        schema = Schema(raw_schema['attributes'], to_one, to_many, auto, allowed)
        self._cache[type_url] = schema
        return schema
