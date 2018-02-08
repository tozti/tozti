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


__all__ = ('UUID_RE', 'router', 'open_db', 'close_db', 'Store')


from json import JSONDecodeError
from uuid import UUID
import logbook

UUID_RE = '-'.join('[0-9a-fA-F]{%d}' % i for i in (8, 4, 4, 4, 12))

# Regex for validating whether a string is a valid type name. 
# Here, valid type names are arbitrary strings with at most one '/' character
# and no '{' or '}'.
TYPE_RE = '([^{}/]+/)?[^{}/]+' 

logger = logbook.Logger('tozti.store')

import tozti
from tozti.utils import (RouterDef, APIError, NotJsonError, BadJsonError,
                         BadDataError, json_response)
from tozti.store.type_schema import Schema


class NoResourceError(APIError):
    code = 'NO_RESOURCE'
    title = 'resource not found'
    status = 404
    template = 'resource {id} not found'


class BadAttrError(APIError):
    code = 'BAD_ATTRIBUTE'
    title = 'an attribute is invalid'
    status = 400


class NoRelError(APIError):
    code = 'BAD_RELATIONSHIP'
    title = 'a relationship is invalid'
    status = 400


class BadRelError(APIError):
    code = 'BAD_RELATIONSHIP'
    title = 'a relationship is invalid'
    status = 400

class BadTypeError(APIError):
    code = 'BAD_TYPE'
    title = 'invalid type'
    status = 404
    template = 'type {type} not found'

from tozti.store.engine import Store


router = RouterDef()
resources = router.add_route('/resources')
resources_single = router.add_route('/resources/{id:%s}' % UUID_RE)
relationship = router.add_route('/resources/{id:%s}/{rel}' % UUID_RE)
types = router.add_route('/types/{type:%s}' % TYPE_RE)

async def get_json_from_request(req):
    if req.content_type != 'application/json':
        raise NotJsonError()
    try:
        data = await req.json()
    except JSONDecodeError:
        raise BadJsonError()
    
    return data

@resources.post
async def resources_post(req):
    """Request handler for ``POST /api/store/resources``."""

    data = await get_json_from_request(req)
    id = await req.app['tozti-store'].create(data)
    return json_response({'data': await req.app['tozti-store'].get(id)})


@resources_single.get
async def resources_get(req):
    """Request handler for ``GET /api/store/resources/{id}``."""

    id = UUID(req.match_info['id'])
    return json_response({'data': await req.app['tozti-store'].get(id)})


@resources_single.patch
async def resources_patch(req):
    """Request handler for ``PATCH /api/store/resources/{id}``."""

    data = await get_json_from_request(req)
    id = UUID(req.match_info['id'])
    await req.app['tozti-store'].update(id, data)
    return json_response({'data': await req.app['tozti-store'].get(id)})


@resources_single.delete
async def resources_delete(req):
    """Request handler for ``DELETE /api/store/resources/{id}``."""

    id = UUID(req.match_info['id'])
    await req.app['tozti-store'].remove(id)
    return json_response({})


@relationship.get
async def relationship_get(req):
    """Request handler for ``GET /api/store/resources/{id}/{rel}``."""

    id = UUID(req.match_info['id'])
    rel = req.match_info['rel']
    return json_response({'data': await req.app['tozti-store'].rel_get(id, rel)})


@relationship.put
async def relationship_put(req):
    """Request handler for ``PUT /api/store/resources/{id}/{rel}``."""

    data = await get_json_from_request(req)
    
    id = UUID(req.match_info['id'])
    rel = req.match_info['rel']

    await req.app['tozti-store'].rel_replace(id, rel, data)
    return json_response({'data': await req.app['tozti-store'].rel_get(id, rel)})


@relationship.post
async def relationship_post(req):
    """Request handler for ``POST /api/store/resources/{id}/{rel}``."""
    
    data = await get_json_from_request(req)
    id = UUID(req.match_info['id'])
    rel = req.match_info['rel']

    await req.app['tozti-store'].rel_append(id, rel, data)
    return json_response({'data': await req.app['tozti-store'].rel_get(id, rel)})

@relationship.delete
async def relationship_delete(req):
    """Request handler for ``DELETE /api/store/resources/{id}/{rel}``"""

    data = await get_json_from_request(req)
    id = UUID(req.match_info['id'])
    rel = req.match_info['rel']

    await req.app['tozti-store'].rel_delete(id, rel, data)
    return json_response({'data': await req.app['tozti-store'].rel_get(id, rel)})

@types.get
async def types_get(req):
    """Request handler for ``GET /api/store/types/{type}``."""
    type = req.match_info['type']

    return json_response({'data': await req.app['tozti-store'].type_get(type)})

async def open_db(app, types):
    """Initialize storage backend at app startup."""

    app['tozti-store'] = Store(types, **tozti.CONFIG['mongodb'])


async def close_db(app):
    """Close storage backend at app cleanup."""

    await app['tozti-store'].close()
