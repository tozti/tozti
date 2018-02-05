from pymacaroons import Macaroon, Verifier
from tozti.auth.utils import (LoginRequired, UnauthorizedRequest)
from tozti.utils import validate, ValidationError
from tozti.core_schemas import SCHEMAS

"""
This decorator is applied to any endpoint for which it is obligated to be
logged in
"""
def must_be_logged(func):
    def function_logged(req, *args, **kwargs):
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
            return True
                
        if not 'auth-token' in req.cookies:
            raise LoginRequired()

        token = req.cookies['auth-token']
        mac = Macaroon.deserialize(token)
        v = Verifier()
        v.satisfy_general(user_exists)

        verified = v.verify(
            mac,
            app.CONFIG['cookie']['private_key']
        )

        if not verified:
            raise LoginRequired()
        
        return func(req, *args, **kwargs)
    return function_logged
    
