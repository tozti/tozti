import pytest
from tests.commons import make_call
from tozti.auth.__init__ import login_post, create_user

def test_macaroon():

    from tozti.auth.utils import create_macaroon
    from tozti.__main__ import load_config_file
    import tozti as tozti_app
    
    tozti_app.CONFIG = load_config_file()
    
    mac = create_macaroon('test', 42, {1:7, 2:9, 3:7}, coucou=2, salut='coucou')
    print(mac.inspect())


# Untested, highly experimental
@pytest.mark.parametrize("json, expected", [
    ({'data':{'type':'core/user', 'attributes':{"name": "Alice", "login": "alice01", "passwd": "passwd_a"}}}, True),
    ({'data':{'type':'core/user', 'attributes':{"name": "Alice", "login": "bob01", "passwd": "passwd_a"}}}, False), # wrong login
    ({'data':{'type':'core/user', 'attributes':{"name": "Alice", "login": "alice01", "passwd": "passwd_b"}}}, False), # wrong passwd
    ({'data':{'type':'core/user', 'attributes':{"name": "Alice", "login": "alice01", "passwd": None}}}, False), # no passwd
    ({'data':{'type':'core/user', 'attributes':{"name": "Alice", "login": None, "passwd": "passwd_a"}}}, False) # no login
    ])
def test_login_post(db, json, expected):
    uid_A = create_user({"type": "core/user", "attributes": {"name": "Alice", "login": "alice01", "passwd": "passwd_a"}})
    uid_B = create_user({"type": "core/user", "attributes": {"name": "Bob", "login": "bob01", "passwd": "passwd_b"}})
    req = make_call("POST", "/auth/login", json=json)
    try:
        ans = login_post(req)
        assert expected
    except:
        assert not expected
