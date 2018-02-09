import json
from pymacaroons import Macaroon, Verifier
import tozti
from tozti.utils import APIError

def create_macaroon(*args, **kwargs):
    mac = Macaroon(
        location=tozti.CONFIG['http']['host'],
        identifier=tozti.CONFIG['cookie']['public_key'],
        key=tozti.CONFIG['cookie']['private_key']
    )

    for a in args:
        mac.add_first_party_caveat(json.dumps(a))
            
    for key, value in kwargs.items():
        mac.add_first_party_caveat('{}={}'.format(json.dumps(key), json.dumps(value)))
    
    return mac

class BadPasswordError(tozti.utils.APIError):
    code = 'Bad_password'
    title = 'Submitted login or password is not valid'
    detail = 'The login/password couple you submited seems to be unknown to our server' 
    status = 400

class LoginRequired(tozti.utils.APIError):
    code = 'Forbidden'
    title = 'Forbidden request'
    detail = 'You must be logged to do this request'
    status = 401

class LoginForbidden(tozti.utils.APIError):
    code = 'Forbidden'
    title = 'Forbidden request'
    detail = 'You must not be logged to do this request'
    status = 401

class UnauthorizedRequest(tozti.utils.APIError):
    code = 'Unauthorized'
    title = 'Unauthorized request'
    detail = 'You are not authorized to do this request'
    status = 403
