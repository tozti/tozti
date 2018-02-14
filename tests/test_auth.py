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

@pytest.mark.parametrize("json, expected", [
    ({"name": "Alice", "login": "alice01", "passwd": "passwd_a", "email": "a@a.com"}, True),
    ({"name": "Alice", "login": "alice01", "passwd": "passwd_a", "email": None}, False),
    ({"name": None, "login": "alice01", "passwd": "passwd_a", "email": "a@a.com"}, False), # noname
    ({"name": "Alice", "login": "alice01", "passwd": None, "email": "a@a.com"}, False), # no passwd
    ({"name": "Alice", "login": None, "passwd": "passwd_a", "email": "a@a.com"}, False) # no login
    ])
def test_login_post(db, json, expected, tozti):
    """ Test user format for create_user and login_post.
    """
    assert (make_call('POST', '/auth/create_user', json=json).status_code == 200) == expected
    assert (make_call("POST", "/auth/login", json=json).status_code == 200) == expected
   
