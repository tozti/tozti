from pymacaroons import Macaroon, Verifier
from tozti.auth.utils import (LoginRequired, UnauthorizedRequest)
from tozti.utils import validate, ValidationError
from tozti.core_schemas import SCHEMAS

def restrict_known_user(func):
    """
    This decorator is applied to any endpoint for which it is obligated to be
    logged in.

    The decorator check if the user is connected (with the req.user field,
    created in the auth_middleware. It raises an error if no user is logged in
    """
    def function_logged(req, *args, **kwargs):
        if req.user == None:
            raise LoginRequired('You must be logged to do this request') 
        return func(req, *args, **kwargs)
    return function_logged

def restrict_not_logged_in(func):
    """
    This decorator is applied to any endpoint for which it is obligated to be
    not logged in.

    The decorator check if the user is connected (with the req.user field,
    created in the auth_middleware. It raises an error if an user is logged in
    """
    def function_not_logged(req, *args, **kwargs):
        if req.user != None:
                raise LoginForbidden('You must not be logged to do this request') 
        return func(req, *args, **kwargs)
    return function_not_logged
    
