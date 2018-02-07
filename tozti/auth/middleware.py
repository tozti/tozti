from aiohttp import web

"""
Middleware that check if a user is logged in the session, and
if this is the case, set its user object in the req object

Usage : in any function, to get access to the current user, juste
use req.user
"""

@web.middleware
def auth_middleware(req, handler):
    app = req.app
    storage = app['tozti-store']

    def user_exists(pred):
        l = pred.split('=')
        if l[0] != "uid":
            return False
        uid = l[1]
        try:
            user = storage.get(uid)
            validate(user, SCHEMAS['user'])
        except KeyError:
            return False
        except ValidationError:
            return False
        req['user'] = user
        return True
            
    if 'auth-token' in req.cookies:
        token = req.cookies['auth-token']
        mac = Macaroon.deserialize(token)
        v = Verifier()
        v.satisfy_general(user_exists)

        verified = v.verify(
            mac,
            app.CONFIG['cookie']['private_key']
        )

        if not verified:
            req.user = None
        else:
            req.user = user
    else:
        req.user = None
    return handler(req)
