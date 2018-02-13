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

from tozti.store import (UUID_RE, logger, NoResourceError, BadAttrError,
                         NoRelError, BadRelError, BadTypeError)
from tozti.utils import BadDataError, ValidationError, validate

from tozti.auth.utils import LoginUnknown as LoginUnknown

#FIXME: how do we get the hostname? config file?
RES_URL = lambda id: '/api/store/resources/%s' % id
REL_URL = lambda id, rel: '/api/store/resources/%s/%s' % (id, rel)

INVALID_UUID = UUID('00000000-0000-0000-0000-000000000000')


# JSON-Schema for incoming data on resource creation.
POST_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'type': { 'type': 'string', 'format': 'uri' },
                'attributes': { 'type': 'object' },
                'relationships': { 'type': 'object' },
            },
            'required': ['type', 'attributes'],
            'additionalProperties': False,
        },
    },
    'required': ['data'],
    'additionalProperties': False,
}

PATCH_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'type': { 'type': 'string', 'format': 'uri' },
                'id': { 'type': 'string', 'pattern': '^%s$' % UUID_RE },
                'attributes': { 'type': 'object' },
                'relationships': { 'type': 'object' },
            },
            'additionalProperties': False,
        },
    },
    'required': ['data'],
    'additionalProperties': False,
}


REL_TO_ONE_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'id': { 'type': 'string', 'pattern': '^%s$' % UUID_RE },
                'type': { 'type': 'string', 'format': 'uri' },
            },
            'required': ['id'],
            'additionalProperties': False,
        },
    },
    'required': ['data'],
    'additionalProperties': False,
}


REL_TO_MANY_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': { 'type': 'string', 'pattern': '^%s$' % UUID_RE },
                    'type': { 'type': 'string', 'format': 'uri' },
                },
                'required': ['id'],
                'additionalProperties': False,
            },
        },
    },
    'required': ['data'],
    'additionalProperties': False,
}


class Store:
    def __init__(self, types, **kwargs):
        self._client = AsyncIOMotorClient(**kwargs)
        self._resources = self._client.tozti.resources
        self._typecache = types

    async def _sanitize_linkage(self, link, types, *, ignore_missing_ids=False):
        """Verify that a given linkage is valid.

        Checks if the target exists and if the given type (if any) is valid.
        Returns the UUID of the target.
        """

        id = UUID(link['id'])
        try:
            type_url = await self.typeof(id)
        except NoResourceError:
            if ignore_missing_ids:
                return id
            else:
                raise BadRelError('linked resource %s does not exist' % id)
        #FIXME: this error leaks type information, check if user can read
        # linked resource first
        if 'type' in link and link['type'] != type_url:
            raise BadRelError('mismatched type for linked resource %s: '
                              'given: %s, real: %s' % (id, link['type'], type_url))
        if types is not None and type_url not in types:
            raise BadRelError('unallowed type %s for linked resource %s' % (
                              type_url, id))
        return id

    async def _sanitize_to_one(self, rel_obj, types):
        """Verify the relationship object and return the UUID of the target."""

        try:
            validate(rel_obj, REL_TO_ONE_SCHEMA)
        except ValidationError as err:
            raise BadRelError('invalid relationship object: %s' % err.message)
        return await self._sanitize_linkage(rel_obj['data'], types)

    async def _sanitize_to_many(self, rel_obj, types, *, ignore_missing_ids=False):
        """Verify the relationship object and return the target UUID list."""

        try:
            validate(rel_obj, REL_TO_MANY_SCHEMA)
        except ValidationError as err:
            raise BadRelError('invalid relationship object: %s' % err.message)

        return_value = []
        for link in rel_obj['data']:
            return_value.append(await self._sanitize_linkage(link, types, ignore_missing_ids=ignore_missing_ids))
        return return_value

    async def _sanitize_attr(self, attr_obj, attr_schema):
        """Verify an attribute value and return it's content."""

        try:
            validate(attr_obj, attr_schema)
        except ValidationError as err:
            raise BadAttrError('invalid attribute: %s' % err.message)
        return attr_obj

    async def _sanitize(self, raw):
        """Verify the content posted for entity creation.

        Returns a partial internal representation, that is a dictionary with
        `type`, `attrs` and `rels` validated.
        """

        try:
            validate(raw, POST_SCHEMA)
        except ValidationError as err:
            raise BadDataError('invalid data: %s' % err.message)

        data = raw['data']
        schema = self._typecache[data['type']]

        attrs = {}
        for (attr, attr_schema) in schema.attrs.items():
            if attr not in data['attributes']:
                raise BadAttrError('attribute not found: %s' % attr)
            attrs[attr] = await self._sanitize_attr(
                data['attributes'].pop(attr), attr_schema)
        if len(data['attributes']) > 0:
                raise BadAttrError('unknown attribute: %s' % data['attributes'].pop())

        rels = {}
        for (rel, types) in schema.to_one.items():
            if rel not in data.get('relationships', {}):
                raise NoRelError('\"%s\" to-one relationships must be defined' % rel)
            rels[rel] = await self._sanitize_to_one(
                data['relationships'].pop(rel), types)

        for (rel, types) in schema.to_many.items():
            if rel not in data.get('relationships', {}):
                rels[rel] = []
                continue
            rels[rel] = await self._sanitize_to_many(
                data['relationships'].pop(rel), types)

        if 'relationships' in data and len(data['relationships']) > 0:
            raise NoRelError('unknown relationship: %s'
                             % data['relationships'].pop())

        return {'type': data['type'], 'attrs': attrs, 'rels': rels}
    
    async def _render_relationship(self, id, rel, type_hint=None):
        """Renders the relationship `rel` belonging to resource with given id. 

        An optional argument `type_hint` can be given in order to avoid querying
        the database for the resource type. Raises a `KeyError` if the resource
        is not found, and a `ValueError` if the relationship is invalid for the
        type of the given resource.
        """

        if type_hint is None:
            rep = await self._resource_by_id(id)
            type_id = rep['type']
        else:
            rep = None
            type_id = type_hint
        schema = self._typecache[type_id]

        if rel in schema.autos:
            return await self._render_auto(id, rel, *schema.autos[rel])
        else:
            if rep is None:
                rep = await self._resource_by_id(id)
            if rel in schema.to_one:
                # at this point we are sure that 'rels' is in rep
                # as the resource is typed
                return await self._render_to_one(id, rel, rep['rels'][rel])
            elif rel in schema.to_many:
                return await self._render_to_many(id, rel, rep['rels'][rel])
            else:
                raise NoRelError('unknown relationship: %s' % rel)

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

        schema = self._typecache[rep['type']]
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

        return_value = {'self': REL_URL(id, rel),
                        'data': []}
        for t in targets:
            return_value['data'].append(await self._render_linkage(t))
        return return_value

    async def _render_auto(self, id, rel, type_url, path):
        """Render a `reverse-of` to-many relationship object."""

        cursor = self._resources.find({'type': type_url,
                                       'rels.%s' % path: id},
                                      {'_id': 1, 'type': 1})
        return_value = {'self': REL_URL(id, rel),
                        'data': []}

        async for hit in cursor:
            return_value['data'].append({'id': hit['_id'],
                                         'type': hit['type'],
                                         'href': RES_URL(hit['_id'])})

        return return_value

    async def create(self, data):
        """Create a new resource and return it's ID.

        The passed data must be the content of the request as specified by
        JSON API. See https://jsonapi.org/format/#crud-creating.
        """

        sanitized = await self._sanitize(data)

        sanitized['_id'] = uuid4()
        current_time = datetime.utcnow().replace(microsecond=0)
        sanitized['created'] = current_time
        sanitized['last-modified'] = current_time

        await self._resources.insert_one(sanitized)
        return sanitized['_id']

    async def set_login_hash(self, login, hash):
        await self._client.tozti.auth.update_one({'login': login}, {'$set': {'hash': hash}}, upsert=True)

    async def _resource_by_id(self, id):
        """Returns the resource with given id.

        `id` must be an instance of `uuid.UUID`. Raises `NoResourceError` if the id
        is not found.
        """

        res = await self._resources.find_one({'_id': id})
        if res is None:
            raise NoResourceError(id=id)
        return res

    async def hash_by_login(self, login):
        """Returns the user_password resource with given login.

        Raises `NoResourceError` if the login is not found.
        """

        res = await self._client.tozti.auth.find_one({'login': login},
                                                     {'hash': 1})
        if res is None:
            raise LoginUnknown('User not found : {}'.format(login))
        return res['hash']

    async def user_uid_by_login(self, login):
        """Returns the user resource with given login.

        Raises `NoResourceError` if the login is not found.
        """

        res = await self._resources.find_one({'type': 'core/user', 'attrs.login': login}, {'_id': 1})
        if res is None:
            raise LoginUnknown('User not found : {}'.format(login))
        
        return res['_id']

    async def typeof(self, id):
        """Return the type URL of a given resource.

        `id` must be an instance of `uuid.UUID`. Raises `KeyError` if the
        resource is not found.
        """

        res = await self._resource_by_id(id)
        return res['type']
        
    async def get(self, id):
        """Query the DB for a resource.

        `id` must be an instance of `uuid.UUID`. Raises `KeyError` if the
        resource is not found. The answer is a JSON API _resource object_.
        See https://jsonapi.org/format/#document-resource-objects.
        """

        logger.debug('querying DB for resource {}'.format(id))
        resp = await self._resource_by_id(id)
        return await self._render(resp)
        
        
    async def update(self, id, raw):
        """Update a resource in the DB.

        `id` must be an instance of `uuid.UUID`. Raises `KeyError` if the
        resource is not found. `raw` must be the content of the request as
        specified by JSON API. See https://jsonapi.org/format/#crud-updating.
        """

        type_id = await self.typeof(id)
        schema = self._typecache[type_id]

        try:
            validate(raw, PATCH_SCHEMA)
        except ValidationError as err:
            raise BadDataError('invalid data: %s' % err.message)
        data = raw['data']

        to_do = {}
        for (attr, value) in data.get('attributes', {}).items():
            if attr not in schema.attrs:
                raise BadAttrError('unknown attribute: %s' % attr)
            san = await self._sanitize_attr(value, schema.attrs[attr])
            to_do['attrs.%s' % attr] = san

        rels = {}
        for (rel, value) in data.get('relationships', {}).items():
            if rel in schema.to_one:
                san = await self._sanitize_to_one(value, schema.to_one[rel])
            elif rel in schema.to_many:
                san = await self._sanitize_to_many(value, schema.to_many[rel])
            elif rel in schema.autos:
                raise BadRelError('cannot update auto relationship: %s' % rel)
            else:
                raise BadRelError('unknown relationship: %s' % rel)
            to_do['rels.%s' % rel] = san

        res = await self._resources.update_one({'_id': id}, {'$set': to_do})
        if res.matched_count == 0:
            # this should never happen
            raise NoResourceError(id=id)

    async def remove(self, id):
        """Remove a resource from the DB.

        `id` must be an instance of `uuid.UUID`. Raises KeyError if the
        resource is not found.
        """

        logger.debug('deleting resource {} from the DB'.format(id))
        result = await self._resources.delete_one({'_id': id})
        if result.deleted_count == 0:
            raise NoResourceError(id=id)

    async def rel_get(self, id, rel):
        try:
            return await self._render_relationship(id, rel)
        except NoRelError as err:
            err.status = 404
            raise err

    async def rel_replace(self, id, rel, data):
        type_id = await self.typeof(id)
        schema = self._typecache[type_id]

        if rel in schema.to_one:
            rel_obj = await self._sanitize_to_one(data, schema.to_one[rel])
        elif rel in schema.to_many:
            rel_obj = await self._sanitize_to_many(data, schema.to_many[rel])
        elif rel in schema.autos:
            raise BadRelError('cannot update auto relationship: %s' % rel,
                              status=404)
        else:
            raise BadRelError('unknown relationship: %s' % rel, status=404)

        res = await self._resources.update_one({'_id': id}, {'$set': {'rels.%s' % rel: rel_obj }})
        if res.matched_count != 1:
            raise NoResourceError(id=id)

    async def rel_append(self, id, rel, data):
        type_id = await self.typeof(id)
        schema = self._typecache[type_id]

        if rel in schema.to_many:
            rel_obj = await self._sanitize_to_many(data, schema.to_many[rel])
        elif rel in schema.to_one:
            raise BadRelError('to-one relationships cannot be posted to', status=403)
        elif rel in schema.autos:
            raise BadRelError('auto relationships cannot be modified', status=403)
        else:
            raise BadRelError('unknown relationship: %s' % rel, status=404)

        res = await self._resources.update_one(
            {'_id': id}, 
            {'$addToSet': {
                'rels.%s' % rel: {
                    '$each': rel_obj
                    }
                }
            })
        if res.matched_count != 1:
            # this should never happen
            raise NoResourceError(id=id)

    async def rel_delete(self, id, rel, data):
        type_id = await self.typeof(id)
        schema = self._typecache[type_id]

        if rel in schema.to_many:
            types = schema.to_many[rel]
        elif rel in schema.to_one:
            raise BadRelError('to-one relationships cannot be deleted', status=403)
        elif rel in schema.autos:
            raise BadRelError('auto relationships cannot be deleted', status=403)
        else:
            raise BadRelError('unknown relationship: %s' % rel, status=404)
        
        ids = await self._sanitize_to_many(data, types, ignore_missing_ids=True)

        res = await self._resources.update_one(
            {'_id': id},
            {'$pullAll': {
                'rels.%s' % rel: ids
            }}
        )

    async def type_get(self, type):
        logger.debug('Querying type %s' % type)
        if type not in self._typecache:
            raise BadTypeError(type=type)
        
        cursor = self._resources.find({'type': type}, ['_id'])
        ret = []
        async for hit in cursor:
            ret.append(await self._render_linkage(hit['_id']))
        return ret

    async def close(self):
        """Close the connection to the MongoDB server."""

        self._client.close()
