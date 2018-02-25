import pytest
from tests.commons import make_call
from tozti.auth.__init__ import login_post, create_user

def test_login_succesfull(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).status_code == 200
    assert make_call('POST', '/auth/login', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).status_code == 200

def test_login_empty(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).status_code == 200
    assert make_call('POST', '/auth/login', json=
            {}).status_code == 400

def test_login_nonexisting(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).status_code == 200
    assert make_call('POST', '/auth/login', json=
            {"name": "b", "handle": "b", "passwd": "a", "email": "a@a.com"}).status_code == 404

def test_login_badpasswd(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).status_code == 200
    assert make_call('POST', '/auth/login', json=
            {"name": "a", "handle": "a", "passwd": "b", "email": "a@a.com"}).status_code == 400

def test_login_incorrect_type(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).status_code == 200
    assert make_call('POST', '/auth/login', json=
            {"name": None, "handle": "b", "passwd": "a", "email": "a@a.com"}).status_code == 404

def test_login_incorrectcontenttype(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "a", "handle": "a", "passwd": "a", "email": "a@a.com"}).status_code == 200
    assert make_call('POST', '/auth/login', json=
        {"name": None, "handle": "b", "passwd": "a", "email": "a@a.com"}, content_type="aé").status_code == 406
