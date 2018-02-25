import pytest
from tests.commons import make_call
from tozti.auth.__init__ import login_post, create_user

def test_register_successfull(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "Alice", "handle": "alice01", "passwd": "passwd_a", "email": "a@a.com"}).status_code == 200

def test_register_incorrectcontenttype(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "Alice", "handle": "alice01", "passwd": "passwd_a", "email": "a@a.com"}, content_type="az").status_code == 406

def test_register_empty(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {}).status_code == 400

def test_register_wrong_mail(db, tozti):
    assert make_call('POST', '/auth/signup', json=
            {"name": "Alice", "handle": "alice01", "passwd": "passwd_a", "email": "a"}).status_code == 400

