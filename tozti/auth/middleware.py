import asyncio
import json
from uuid import UUID

from aiohttp import web
from pymacaroons import Macaroon, Verifier

import tozti
from tozti.store import NoResourceError


@web.middleware
async def auth_middleware(req, handler):
    """
    Middleware that check if a user is logged in the session, and
    if this is the case, set its user object in the req object

    Usage : in any function, to get access to the current user, juste
    use req.user
    """
    app = req.app
    storage = app['tozti-store']
    user_uid = None

    def user_exists(cookie):
        nonlocal user_uid
        dictio = json.loads(cookie)
        uid = UUID(dictio['uid'])
        user_uid = uid
        return True

    if 'auth-token' in req.cookies:
        token = req.cookies['auth-token']
        mac = Macaroon.deserialize(token)
        v = Verifier()
        v.satisfy_general(user_exists)
        try:
            verified = v.verify(
                mac,
                tozti.CONFIG['cookie']['private_key']
            )
        except:
            req['user'] = None
        else:
            try:
                user = await storage.resource_by_id(user_uid)
                print(user)
                if user["type"] != "core/user":
                    req['user'] = None
                else:
                    req['user'] = user['_id']
            except NoResourceError:
                req['user'] = None

    else:
        req['user'] = None
    return await handler(req)
