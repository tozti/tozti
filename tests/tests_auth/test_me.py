import pytest
from tests.commons import make_call
from tozti.auth.__init__ import login_post, create_user
from tests.commons import db_contains_object, make_call, add_object_get_id
from tozti.auth.utils import create_macaroon
from tozti.__main__ import load_config_file
import requests
import tozti as tozti_app

def test_me_succesfull(db, tozti):
    uid = make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).json()["uid"]
    result = make_call('POST', '/auth/login', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"})
    cookies = result.cookies
    result = make_call('GET', '/auth/me', cookies=cookies)
    assert result.json()["data"] == uid


def test_me_empty(db, tozti):
    result = make_call('GET', '/auth/me', cookies={})
    assert result.status_code == 401


@pytest.mark.extensions("rel01")
def test_me_forged_bad_uuid(db, tozti):
    tozti_app.CONFIG = load_config_file()
    mac = create_macaroon({'handle': "a", 'uid': "00000000-0000-0000-0000-000000000000"}) 
    jar = requests.cookies.RequestsCookieJar()
    jar.set('auth-token', mac.serialize()) 
    result = make_call('GET', '/auth/me', cookies=jar)
    assert result.status_code == 401

@pytest.mark.extensions("rel01")
def test_me_forged_bad_ressource_type(db, tozti):
    uid_bar = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    tozti_app.CONFIG = load_config_file()
    mac = create_macaroon({'handle': "b", 'uid': str(uid_bar)}) 
    jar = requests.cookies.RequestsCookieJar()
    jar.set('auth-token', mac.serialize()) 
    result = make_call('GET', '/auth/me', cookies=jar)
    assert result.status_code == 401

def test_me_forged_bad_key(db, tozti):
    uid = make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).json()["uid"]
    tozti_app.CONFIG = load_config_file()
    tozti_app.CONFIG["cookie"]["public_key"] = "a"
    tozti_app.CONFIG["cookie"]["private_key"] = "a"
    mac = create_macaroon({'handle': "a", 'uid': str(uid)}) 
    jar = requests.cookies.RequestsCookieJar()
    jar.set('auth-token', mac.serialize()) 
    result = make_call('GET', '/auth/me', cookies=jar)
    assert result.status_code == 401
