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


from json import JSONDecodeError
from collections import namedtuple
from datetime import datetime, timezone
from uuid import uuid4, UUID

import aiohttp
from aiohttp.web import json_response
import jsonschema
from jsonschema.exceptions import ValidationError
from motor.motor_asyncio import AsyncIOMotorClient

from tozti import logger
from tozti.utils import RouterDef, register_error, api_error


register_error('RESOURCE_NOT_FOUND', 'resource {id} not found', 404)
register_error('NOT_JSON', 'expected json data', 406)
register_error('BAD_JSON', 'malformated json data', 400)
register_error('INVALID_DATA', 'invalid submission: {err}', 400)


########
# Routes

router = RouterDef()

uuid_re = '-'.join('[0-9a-fA-F]{%d}' % i for i in (8, 4, 4, 4, 12))
relationship_re = r'[\da-z]+'
resources = router.add_route('/resources')
resources_single = router.add_route('/resources/{id:%s}' % uuid_re)
relationship = router.add_route('/resources/{id:%s}/{rel:%s}' % (uuid_re, relationship_re))


@resources.post
async def resources_post(req):
    """POST /api/store/resources
    """
    if req.content_type != 'application/json':
        return api_error('NOT_JSON')
    try:
        data = await req.json()
    except JSONDecodeError:
        return api_error('BAD_JSON')
    try:
        id = await req.app['tozti-store'].create(data)
    except ValueError as err:
        return api_error('INVALID_DATA', err=err)
    return json_response(await req.app['tozti-store'].get(id))


@resources_single.get
async def resources_get(req):
    """GET /api/store/resources
    """
    id = req.match_info['id']
    try:
        return json_response(await req.app['tozti-store'].get(id))
    except KeyError:
        return api_error('RESOURCE_NOT_FOUND', id=id)

@resources_single.patch
async def resources_patch(req):
    pass

@resources_single.delete
async def resources_delete(req):
    id = req.match_info['id']
    try:
        req.app['tozti-store'].remove(id)
    except KeyError:
        return api_error('RESOURCE_NOT_FOUND', id=id)


@relationship.get
async def relationship_get(req):
    id = req.match_info['id']
    rel = req.match_info['rel']
    try:
        resp = await req.app['tozti-store'].get(id)
        return json_response(resp[rel])
    except KeyError:
        return api_error('RESOURCE_NOT_FOUND', id=id)

@relationship.put
async def relationship_put(req):
    pass

@relationship.post
async def relationship_post(req):
    pass


#########
# Backend

async def open_db(app):
    """Initialize storage backend at app startup."""
    app['tozti-store'] = Store(**app['tozti-config']['mongodb'])


async def close_db(app):
    """Close storage backend at app cleanup."""
    await app['tozti-store'].close()


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

        await self._typecache.validate(data)
        await self._resources.insert_one(data)

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
