import pytest
from tests.commons import make_call
from tozti.auth.__init__ import login_post, create_user
from tests.commons import db_contains_object, make_call, add_object_get_id
from tozti.auth.utils import create_macaroon
from tozti.__main__ import load_config_file
import requests
import tozti as tozti_app

def test_is_logged_succesfull(db, tozti):
    uid = make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).json()["uid"]
    result = make_call('POST', '/auth/login', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"})
    cookies = result.cookies
    result = make_call('GET', '/auth/is_logged', cookies=cookies)
    assert result.status_code == 200


def test_is_logged_empty(db, tozti):
    result = make_call('GET', '/auth/is_logged', cookies={})
    assert result.status_code == 401
