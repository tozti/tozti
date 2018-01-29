import json
from pymacaroons import Macaroon, Verifier
import tozti

def place_macaroon(app, response, title, m):
    response.cookie[title] = m.serialize()

def create_macaroon(*args, **kwargs):
    mac = Macaroon(
        location=tozti.CONFIG['http']['host'],
        identifier=tozti.CONFIG['cookie']['public_key'],
        key=tozti.CONFIG['cookie']['private_key']
    )

    for a in args:
        mac.add_first_party_caveat(json.dumps(a))
        
    
    for key, value in kwargs.items():
        mac.add_first_party_caveat('{} = {}'.format(json.dumps(key), json.dumps(value)))
    
    return mac
