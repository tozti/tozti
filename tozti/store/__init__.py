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

from tozti.utils import RouterDef, register_error, api_error, json_response
from tozti.store.engine import Store


register_error('RESOURCE_NOT_FOUND', 'resource {id} not found', 404)
register_error('NOT_JSON', 'expected json data', 406)
register_error('BAD_JSON', 'malformated json data', 400)
register_error('INVALID_DATA', 'invalid submission: {err}', 400)


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
