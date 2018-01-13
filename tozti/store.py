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

uuid_re = '-'.join('[0-9a-fA-F]{%d}' % i for i in (8, 4, 4, 4, 12))
resources = router.add_resource('/resources')
resources_single = router.add_resource('/resources/{rid:%s}' % uuid_re)
relationship = router.add_resource('/resources/{rid:%s}/{rel}' % uuid_re)


@resources.post
async def resources_post(req):
    pass

@resources_single.get
async def resources_get(req):
    pass

@resources_single.patch
async def resources_patch(req):
    pass

@resources_single.delete
async def resources_delete(req):
    pass

@relationship.get
async def relationship_get(req):
    pass

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
    app['tozti-store'] = EntityStore(**app['tozti-config']['mongodb'])


async def close_db(app):
    """Close storage backend at app cleanup."""
    await app['tozti-store'].close()


class Store:
    def __init__(self, **kwargs):
        self._client = AsyncIOMotorClient(**kwargs)
        self._resources = self._client.tozti.resources
        self._typecache = {}

    async def _render(self, internal):
        """Take internal rep and return it in an HTTP-API valid format."""
        return {}

    async def create(self, data):
        """Take python dict from http request and add it to the db."""
        return

    async def get(self, id):
        return

    async def update(self, id, data):
        return

    async def remove(self, id):
        return

    async def rel_get(self, id, rel):
        return

    async def rel_update(self, id, rel, data):
        return

    async def rel_append(self, id, rel, data)

    async def close():
        pass
