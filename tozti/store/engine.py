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
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from tozti.store import logger, NoResourceError, NoTypeError, BadItemError, NoItemError, NoHandleError
from tozti.store.schema import Schema, fmt_resource_url
from tozti.utils import BadDataError, ValidationError, validate

from tozti.auth.utils import LoginUnknown as LoginUnknown


class Store:
    def __init__(self, types, **kwargs):
        self._client = AsyncIOMotorClient(**kwargs)
        self._db = self._client.tozti
        self._types = {k: Schema(k, v, db=self) for (k, v) in types.items()}

    async def resource_by_id(self, id, projection=None):
        """Returns the raw resource with given id.

        `id` must be an instance of `uuid.UUID`. Raises `NoResourceError` if
        the resource is not found.
        """

        logger.debug('querying DB for resource {}'.format(id))
        res = await self._db.resources.find_one({'_id': id}, projection=projection)
        if res is None:
            raise NoResourceError(id=id)
        return res

    async def type_by_id(self, id):
        """Return the type URL of a given resource.

        `id` must be an instance of `uuid.UUID`. Raises `NoResourceError` if
        the resource is not found.
        """

        logger.debug('querying DB for type of resource {}'.format(id))
        res = await self.resource_by_id(id, {'type': 1})
        return res['type']

    async def create(self, raw):
        """Create a new resource and return it's rendered form.

        The passed data must be the content of the request as specified by
        JSON API. See https://jsonapi.org/format/#crud-creating.
        """

        try:
            tp = raw['data']['type']
        except (TypeError, KeyError):
            raise BadDataError('invalid data: type must be specified')

        if tp not in self._types:
            raise NoTypeError(type=tp)
        schema = self._types[tp]

        data = await schema.sanitize(raw)
        data['_id'] = uuid4()
        current_time = datetime.utcnow().replace(microsecond=0)
        data['created'] = current_time
        data['last-modified'] = current_time
        await self._db.resources.insert_one(data)

        return await schema.render(data)

    async def read(self, id):
        """Query the DB for a resource.

        `id` must be an instance of `uuid.UUID`. Raises `NoResourceError` if
        the resource is not found. The answer is a JSON API _resource object_.
        See https://jsonapi.org/format/#document-resource-objects.
        """

        res = await self.resource_by_id(id)
        schema = self._types[res['type']]
        return await schema.render(res)

    async def update(self, id, raw):
        """Update a resource in the DB.

        `id` must be an instance of `uuid.UUID`. Raises `NoResourceError` if
        the resource is not found. `raw` must be the content of the request as
        specified by JSON API. See https://jsonapi.org/format/#crud-updating.
        """

        schema = self._types[await self.type_by_id(id)]
        data = await schema.sanitize(raw, is_create=False)
        if len(data) > 0:
            await self._db.resources.update_one({'_id': id}, {'$set': data})

    async def delete(self, id):
        """Remove a resource from the DB.

        `id` must be an instance of `uuid.UUID`. Raises KeyError if the
        resource is not found.
        """

        logger.debug('Deleting resource {} from the DB'.format(id))
        result = await self._db.resources.delete_one({'_id': id})
        if result.deleted_count == 0:
            raise NoResourceError(id=id)

    async def item_read(self, id, key):
        schema = self._types[await self.type_by_id(id)]
        if key not in schema:
            raise NoItemError(key=key, status=404)

        data = await self.resource_by_id(id, {'body.%s' % key: 1})
        return await schema[key].render(id, data['body'].get(key))

    async def item_update(self, id, key, raw):
        schema = self._types[await self.type_by_id(id)]

        try:
            data = await schema[key].sanitize(raw)
        except NoItemError as err:
            err.status = 404
            raise err

        await self._db.resources.update_one(
            {'_id': id},
            {'$set': {'body.%s' % key: data}})

    async def item_append(self, id, key, raw):
        schema = self._types[await self.type_by_id(id)]

        if key not in schema:
            raise NoItemError(key=key, status=404)

        if not schema[key].is_array:
            raise BadItemError('body item {key} is not an array', key=key)

        print(raw)

        data = await schema[key].sanitize(raw)

        await self._db.resources.update_one(
            {'_id': id},
            {'$addToSet': {'body.%s' % key: {'$each': data}}})

    async def item_remove(self, id, key, raw):
        schema = self._types[await self.type_by_id(id)]

        if key not in schema:
            raise NoItemError(key=key, status=404)

        if not schema[key].is_array:
            raise BadItemError('body item {key} is not an array', key=key)

        data = await schema[key].sanitize(raw, check_consistency=False)
        print(data)

        await self._db.resources.update_one(
            {'_id': id},
            {'$pull': {'body.%s' % key: {'id': {'$in': [UUID(x['id']) for x in data]}}}})

    async def resources_by_type(self, type):
        logger.debug('Querying type %s' % type)
        if type not in self._types:
            raise NoTypeError(type=type, status=404)

        cursor = self._db.resources.find({'type': type}, ['_id'])
        links = []
        async for hit in cursor:
            links.append({'id': hit['_id'],
                          'type': type,
                          'href': fmt_resource_url(hit['_id'])})
        return links

    async def by_handle(self, handle):
        doc = self._db.handles.find_one({'_id': handle})
        if doc is None:
            raise NoHandleError(handle=handle)
        return {'id': doc['target'],
                'type': doc['type'],
                'href': fmt_resource_url(doc['target'])}

    async def set_handle(self, handle, id):
        

    async def close(self):
        """Close the connection to the MongoDB server."""

        self._client.close()
