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


from datetime import datetime, timezone
from uuid import uuid4, UUID

import jsonschema
from motor.motor_asyncio import AsyncIOMotorClient

from tozti import logger
from tozti.store.typecache import TypeCache


#FIXME: how do we get the hostname? config file?
BASE_URL = 'http://localhost'
RES_URL = lambda id: '%s/resources/%s' % (BASE_URL, id)
REL_URL = lambda id, rel: '%s/resources/%s/%s' % (BASE_URL, id, rel)


class Store:
    def __init__(self, **kwargs):
        self._client = AsyncIOMotorClient(**kwargs)
        self._resources = self._client.tozti.resources
        self._typecache = TypeCache()

    async def sanitize_incoming(self, data):
        allowed_keys = {'type', 'attributes', 'meta', 'relationships'}
        if not data.keys() <= allowed_keys:
            raise ValueError('unknown key')

        try:
            type = data['type']
        except KeyError:
            raise ValueError('no type specified')
        schema = await self._typecache[type]

        output = {
            'type': type,
            'relationships': {}
        }

        try:
            print("Validating", data['attributes'], "against", schema.attributes)
            jsonschema.validate(data['attributes'], schema.attributes)
        except ValidationError as err:
            raise ValueError(err.message)
        output['attributes'] = attributes

        rels = data.get('relationships', {})
        if not rels.keys() <= schema.allowed_rels:
            raise ValueError('unknown relationship')

        for (rel, target) in schema.to_one:
            if not rel in rels:
                output['relationships'][rel] = UUID('00000000-0000-0000-0000-000000000000')
                continue
            if not rels[rel].keys() == {'data'}:
                raise ValueError('bad relationship object')
            if 'id' not in rels[rel]['data']:
                raise ValueError('bad relationship object')
            id = rels[rel]['data']['id']
            try:
                tp = await self.typeof(id)
            except KeyError:
                raise ValueError('unknown target object')
            if not tp == rels[rel]['data'].get('type', tp):
                raise ValueError('type mismatch')
            output['relationships'][rel] = id

        for (rel, target) in schema.to_many:
            if not rel in rels:
                output['relationships'][rel] = []
                continue
            if not rels[rel].keys() == {'data'}:
                raise ValueError('bad relationship object')
            out_rels = []
            for rel_obj in rels[rel]['data']:
                if 'id' not in rel_obj:
                    raise ValueError('bad relationship object')
                id = rel_obj['id']
                try:
                    tp = await self.typeof(id)
                except KeyError:
                    raise ValueError('unknown target object')
                if not tp == rel_obj.get('type', tp):
                    raise ValueError('type mismatch')
                out_rels.append(id)
            output['relationships'] = out_rels

        return output


    async def _render(self, rep):
        """Take internal representation and return it in an HTTP-API format."""

        id = rep['_id']

        out = {
            'type': rep['type'],
            'id': id,
            'attributes': rep['attributes'],
            'meta': {
                'created': rep['created'],
                'last-modified': rep['last-modified'],
            },
            'relationships': {
                'self': {'data': {'href': RES_URL(id), 'id': id, 'type': rep['type']}},
            },
        }

        schema = await self._typecache[rep['type']]
        for (rel, _) in schema.to_one:
            target = rep['relationships'][rel]
            out['relationships'][rel] = {
                'self': REL_URL(id, rel),
                'data': {
                    'id': target,
                    'type': await self.typeof(target),
                    'href': RES_URL(target),
                }
            }
        for (rel, _) in schema.to_many:
            data = [{'href': RES_URL(i), 'type': await self.typeof(i), 'id': i}
                    for i in rep['relationships'][rel]]
            out['relationships'][rel] = {
                'self': REL_URL(id, rel),
                'data': data,
            }
        for (rel, defs) in schema.auto:
            data = await self._resources.find({'type': defs['type'],
                                               'relationships': {defs['path']: id}})
            out['relationships'][rel] = {
                'self': REL_URL(id, rel),
                'data': [{'type': d['type'], 'id': d['_id'], 'href': RES_URL(d['_id'])} for d in data]
            }


        return out

    async def create(self, data):
        """Take python dict from http request and add it to the db."""
        logger.debug('incoming data: {}'.format(data))
        if 'type' not in data:
            raise ValueError('missing type property')

        # sanitization, keep just the allowed non-autogenerated properties
        attributes = data.get('attributes', {})
        relationships = data.get('relationships', {})
        meta = data.get('meta', {})
        resource_type = data['type']
        data = {'attributes': attributes, 'relationships': relationships,
                'meta': meta, 'type': resource_type}

        sanitized = await self.sanitize_incoming(data)
        sanitized['_id'] = uuid4()
        await self._resources.insert_one(sanitized)

    async def typeof(self, id):
        pass

    async def get(self, id):
        logger.debug('querying DB for resource {}'.format(id))
        resp = await self._resources.find_one({'_id': id})
        if resp is None:
            raise KeyError
        return await self._render(resp)

    async def update(self, id, data):
        pass

    async def remove(self, id):
        logger.debug('deleting resource {} from the DB'.format(id))
        result = await self._resources.delete_one({'_id': id})
        if result.deleted_count == 0:
            raise KeyError

    async def rel_get(self, id, rel):
        pass

    async def rel_update(self, id, rel, data):
        pass

    async def rel_append(self, id, rel, data):
        pass

    async def close(self):
        pass
