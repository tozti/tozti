from pymacaroons import Macaroon, Verifier
from tozti.auth.utils import (LoginRequired, UnauthorizedRequest)
from tozti.utils import validate, ValidationError
from tozti.core_schemas import SCHEMAS

"""
This decorator is applied to any endpoint for which it is obligated to be
logged in.

The decorator check if the user is connected (with the req.user field,
created in the auth_middleware. It raises an error if no user is logged in
"""
def restrict_known_user(func):
    def function_logged(req, *args, **kwargs):
        if req.user == None:
            raise LoginRequired() 
        return func(req, *args, **kwargs)
    return function_logged
    
