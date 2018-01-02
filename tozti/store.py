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
from datetime import datetime, timezone
from uuid import uuid4


from aiohttp.web import json_response
from motor.motor_asyncio import AsyncIOMotorClient

from tozti import logger
from tozti.utils import RouterDef, register_error, api_error


register_error('ENTITY_NOT_FOUND', 'entity {eid} not found', 404)
register_error('NOT_JSON', 'expected json data', 406)
register_error('BAD_JSON', 'malformated json data', 400)
register_error('INVALID_ENTITY', 'invalid entity content: {err}', 400)


########
# Routes

router = RouterDef()

entity = router.add_resource('/entity')

uuid_re = '-'.join('[0-9a-fA-F]{%d}' % i for i in (8, 4, 4, 4, 12))
entity_single = router.add_resource('/entity/{eid:%s}' % uuid_re)



@entity.post
async def entity_post(req):
    """POST /api/store/entity

    Returns newly created entity.
    """

    if req.content_type != 'application/json':
        return api_error('NOT_JSON')
    try:
        data = await req.json()
    except JSONDecodeError:
        return api_error('BAD_JSON')
    try:
        eid = await req.app['tozti-store'].create_entity(data)
    except ValueError as err:
        return api_error('INVALID_ENTITY', err=err)
    return json_response(await req.app['tozti-store'].get_entity(eid))

@entity_single.get
async def entity_get(req):
    """GET /api/store/entity/{eid}

    Returns matching entity if existing and readable.
    """

    eid = req.match_info['eid']
    try:
        return json_response(await req.app['tozti-store'].get_entity(eid))
    except KeyError:
        return api_error('ENTITY_NOT_FOUND', eid=eid)


#########
# Backend

async def open_db(app):
    """Initialize storage backend at app startup."""
    app['tozti-store'] = EntityStore(**app['tozti-config']['mongodb'])


async def close_db(app):
    """Close storage backend at app cleanup."""
    await app['tozti-store'].close()


class EntityStore:
    def __init__(self, **kwargs):
        self._client = AsyncIOMotorClient(**kwargs)
        self._entities = self._client.tozti.entities

    async def get_entity(self, eid):
        logger.debug('querying DB for entity {}'.format(eid))
        resp = await self._entities.find_one({'eid': eid})
        if resp is None:
            raise KeyError
        del resp['_id']
        resp['creation'] = resp['creation'].isoformat()
        resp['last-edit'] = resp['last-edit'].isoformat()
        return resp

    async def close(self):
        self._client.close()

    async def create_entity(self, data):
        logger.debug('incoming data: {}'.format(data))
        if 'type' not in data:
            raise ValueError('missing type property')

        # complete the metadata
        eid = str(uuid4())
        now = datetime.now(timezone.utc).replace(microsecond=0)
        data['creation'] = now
        data['last-edit'] = now
        data['eid'] = eid

        await self._entities.insert_one(data)
        return eid
