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
from jsonschema.exceptions import ValidationError
from motor.motor_asyncio import AsyncIOMotorClient

from tozti import logger
from tozti.store.typecache import TypeCache


#FIXME: how do we get the hostname? config file?
RES_URL = lambda id: '/api/store/resources/%s' % id
REL_URL = lambda id, rel: '/api/store/resources/%s/%s' % (id, rel)

INVALID_UUID = UUID('00000000-0000-0000-0000-000000000000')


# JSON-Schema for incoming data on resource creation.
INPUT_SCHEMA = {
    'type': 'object',
    'properties': {
        'type': { 'type': 'string', 'format': 'uri' },
        'attributes': { 'type': 'object' },
        'relationships': { 'type': 'object' },
    },
    'required': ['type', 'attributes'],
}


class Store:
    def __init__(self, **kwargs):
        self._client = AsyncIOMotorClient(**kwargs)
        self._resources = self._client.tozti.resources
        self._typecache = TypeCache()

    async def _sanitize_linkage(self, link):
        """Verify that a given linkage is valid.

        Checks if the target exists and if the given type (if any) is valid.
        Returns the UUID of the target.
        """

        id = UUID(link['id'])
        try:
            type_url = await self.typeof(id)
        except KeyError:
            raise ValueError('linked resource %s does not exist' % id)
        if 'type' in link and link['type'] != type_url:
            raise ValueError('mismatched type for linked resource %s: '
                             'given: %s, real: %s' % (id, link['type'], type_url))
        return id


    async def _sanitize(self, data):
        """Verify the content posted for entity creation.

        Returns a partial internal representation, that is a dictionary with
        `type`, `attrs` and `rels` validated.
        """

        try:
            jsonschema.validate(data, INPUT_SCHEMA)
        except ValidationError as err:
            raise ValueError('invalid data: %s' % err)

        schema = await self._typecache[data['type']]

        attrs = {}
        for (attr, attr_schema) in schema.attrs.items():
            if attr not in data['attributes']:
                raise ValueError('attribute %s not found' % attr)
            attr_obj = data['attributes'].pop(attr)
            try:
                jsonschema.validate(attr_obj, schema.attrs[attr])
            except ValidationError as err:
                raise ValueError('invalid attribute %s: %s' % (attr, err))
            attrs[attr] = attr_obj
        if len(data['attributes']) > 0:
                raise ValueError('unknown attribute %s' % data['attributes'].pop())

        rels = {}
        for (rel, rel_schema) in schema.to_one.items():
            if rel not in data['relationships']:
                rels[rel] = INVALID_UUID
                continue
            rel_obj = data['relationships'].pop(rel)
            try:
                jsonschema.validate(rel_obj, rel_schema)
            except ValidationError as err:
                raise ValueError('invalid relationship %s: %s' % (rel, err))
            rels[rel] = await self._sanitize_linkage(rel_obj['data'])

        for (rel, rel_schema) in schema.to_many.items():
            if rel not in data['relationships']:
                rels[rel] = []
                continue
            rel_obj = data['relationships'].pop(rel)
            try:
                jsonschema.validate(rel_obj, rel_schema)
            except ValidationError as err:
                raise ValueError('invalid relationship %s: %s' % (rel, err))
            rels[rel] = [await self._sanitize_linkage(link)
                         for link in rel_obj['data']]

        if 'relationships' in data and len(data['relationships']) > 0:
            raise ValueError('unknown relationship: %s'
                             % data['relationships'].pop())

        return {'type': data['type'], 'attrs': attrs, 'rels': rels}

    async def _render(self, rep):
        """Render a resource object given it's internal representation.

        See https://jsonapi.org/format/#document-resource-objects.
        """

        id = rep['_id']

        rels = {'self': await self._render_to_one(id, 'self', id)}

        for (rel, rel_obj) in rep['rels'].items():
            if isinstance(rel_obj, UUID):
                rels[rel] = await self._render_to_one(id, rel, rel_obj)
            else:
                rels[rel] = await self._render_to_many(id, rel, rel_obj)

        schema = await self._typecache[rep['type']]
        for (rel, auto_def) in schema.autos.items():
            rels[rel] = await self._render_auto(id, rel, *auto_def)

        return {'id': id,
                'type': rep['type'],
                'attributes': rep['attrs'],
                'relationships': rels,
                'meta': {'created': rep['created'],
                         'last-modified': rep['last-modified']}}

    async def _render_linkage(self, target):
        """Render a resource object linkage.

        Does not catch KeyError in case the target is not found. The divergence
        from the spec is that we include an `href` property which is an URI
        resolving to the given target resource.

        See https://jsonapi.org/format/#document-resource-object-linkage.
        """

        return {'id': target,
                'type': await self.typeof(target),
                'href': RES_URL(target)}

    async def _render_to_one(self, id, rel, target):
        """Render a to-one relationship object.

        See https://jsonapi.org/format/#document-resource-object-relationships.
        """

        return {'self': REL_URL(id, rel),
                'data': await self._render_linkage(target)}

    async def _render_to_many(self, id, rel, targets):
        """Render a to-many relationship object.

        See https://jsonapi.org/format/#document-resource-object-relationships.
        """

        return {'self': REL_URL(id, rel),
                'data': [await self._render_linkage(t) for t in targets]}

    async def _render_auto(self, id, rel, type_url, path):
        """Render a `reverse-of` to-many relationship object."""

        cursor = self._resources.find({'type': type_url,
                                       'rels.%s' % path: id},
                                      {'_id': 1, 'type': 1})
        return {'self': REL_URL(id, rel),
                'data': [{'id': hit['_id'],
                          'type': hit['type'],
                          'href': RES_URL(hit['_id'])}
                         async for hit in cursor]}

    async def create(self, data):
        """Take python dict from http request and add it to the db."""

        logger.debug('incoming data: {}'.format(data))
        if 'type' not in data:
            raise ValueError('missing type property')

        sanitized = await self._sanitize(data)

        sanitized['_id'] = uuid4()
        current_time = datetime.utcnow().replace(microsecond=0)
        sanitized['created'] = current_time
        sanitized['last-modified'] = current_time

        ret = await self._resources.insert_one(sanitized)
        return sanitized['_id']

    async def typeof(self, id):
        res = await self._resources.find_one({'_id': id}, {'type': 1})
        if res is None:
            raise KeyError
        return res['type']

    async def get(self, id):
        logger.debug('querying DB for resource {}'.format(id))
        resp = await self._resources.find_one({'_id': id})
        if resp is None:
            raise KeyError
        return await self._render(resp)

    async def update(self, id, data):
        resource_type = await self.typeof(id)
        schema = await self._typecache[resource_type]
        allowed_attributes = schema.attributes
        for attr, value in data['attributes'].items():
            schema = allowed_attributes.get(attr, None)
            if schema is None:
                raise ValueError("invalid attribute {}".format(attr))
            jsonschema.validate(value, schema)

        res = await self._resources.update_one({'_id': id}, { '$set': data})
        if res.matched_count == 0:
            raise KeyError

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
        self._client.close()
