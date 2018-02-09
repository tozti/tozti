
def test_macaroon():

    from tozti.auth.utils import create_macaroon
    from tozti.__main__ import load_config_file
    import tozti as tozti_app
    
    tozti_app.CONFIG = load_config_file()
    
    mac = create_macaroon('test', 42, {1:7, 2:9, 3:7}, coucou=2, salut='coucou')
    print(mac.inspect())


# Untested, highly experimental
@pytest.mark.parametrize("json, expected", [
    ({"login": "Alice", "passwd": "passwd_a"}, True),
    ({"login": "Bob", "passwd": "passwd_a"}, False), # wrong login
    ({"login": "Alice", "passwd": "passwd_b"}, False), # wrong passwd
    ({"login": "Alice", "passwd": None}, False), # no passwd
    ({"login": None, "passwd": "passwd_a"}, False) # no login
    ])
def test_login_post(db, json):
    uid_A = add_object_get_id({"type": "core/user", "attributes": {"login": "Alice", "passwd": "passwd_a"}})
    uid_B = add_object_get_id({"type": "core/user", "attributes": {"login": "Bob", "passwd": "passwd_b"}})
    req = make_call("POST", "/auth/login", json=json)
    try:
        ans = login_post(req)
        assert expected
    except:
        assert not expected
