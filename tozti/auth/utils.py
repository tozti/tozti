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
    status = 400

class LoginRequired(tozti.utils.APIError):
    code = 'Forbidden'
    title = 'Forbidden request'
    status = 401

class LoginForbidden(tozti.utils.APIError):
    code = 'Forbidden'
    title = 'Forbidden request'
    status = 401

class UnauthorizedRequest(tozti.utils.APIError):
    code = 'Unauthorized'
    title = 'Unauthorized request'
    status = 403

class LoginUnknown(tozti.utils.APIError):
    code = 'Login_unknown'
    title = 'Login not known'
    status = 400

