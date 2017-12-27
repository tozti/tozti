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


from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from tozti.utils import RouterDef, api_error


router = RouterDef()
entity = router.add_resource('/entity/{eid:[0-9a-f]{8,8}}')


@entity.get
async def entity_get(req):
    entity = await req.app['tozti-store'].get_entity(
        int(req.match_info['eid'], 16))
    return web.json_response(entity)


async def open_db(app):
    """Initialize storage backend at app startup."""
    app['tozti-store'] = EntityStore(**app['tozti-config']['mongodb'])


async def close_db(app):
    """Close storage backend at app cleanup."""
    await app['tozti-store'].close()


class EntityStore:
    def __init__(self, **kwargs):
        db = kwargs.pop('db', 'tozti')
        self._db_name = db
        self._client = AsyncIOMotorClient(**kwargs)
        self.db = self._client[db]
        

    async def get_entity(self, eid):
        return await self.db.entities.find_one({'eid': eid})

    async def close(self):
        self._client.close()
