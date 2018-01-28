from tests.commons import launch_tozti, stop_tozti, tozti
import json
from requests import get, post, put, patch, delete
import requests
from pymongo import MongoClient
import pytest


API = 'http://127.0.0.1:8080/api'
TYPE = "type/foo"


"""
@pytest.fixture(scope="module")
def tozti(request):
    tozti = launch_tozti()
    if tozti is None:
        assert False

    yield tozti

    def end():
        stop_tozti(tozti)
    request.addfinalizer(end)
"""

@pytest.fixture(scope="module")
def load_db(request):
    client = MongoClient(host="localhost", port=27017)
    yield client.tozti.resources
    request.addfinalizer(lambda: client.close())

@pytest.fixture(scope="function")
def db(load_db):
    load_db.drop()
    yield load_db


def make_call(meth, path, json=None):
    return requests.request(meth, API + path, json=json)

def check_call(meth, path, json=None):
    resp = requests.request(meth, API + path, json=json)
    ans = resp.json()
    return 'errors' in ans


def db_is_object(db, obj):
    """Check if the database only contains object obj
    """
    if db.count() == 1:
        for o in db.find():
            if o["attrs"] != obj["attributes"]:
                return False
        return True
    return False


def add_object_get_id(obj):
    """Insert the object defined by `obj` into the database
    And returns the associated id
    """
    ret_val = make_call("POST", '/store/resources', json={"data": obj}).json()
    return ret_val['data']['id']


@pytest.mark.extensions("type")
@pytest.mark.parametrize("json, expected", [
    ({"type": TYPE, "attributes": {"name": "f", "email": "a@a.com"}},   True),
    ({"type": TYPE, "atxtributes": {"name": "f", "email": "a@a.com"}},  False),
    ({"type": TYPE, "attributes": {"name": "f", "email": "a"}},         False),
    ({"type": TYPE, "attributes": {"name": "f"}},                       False),
    ({"type": TYPE, "attributes": {"name": "f", "foo": "b"}},           False)
    ])
def test_storage_post_request(tozti, db, json, expected):
    ret_val = make_call("POST", '/store/resources', json={"data": json})
    if ret_val.status_code == 200:
        assert db_is_object(db, json) == expected
    else:
        assert not expected

def test_storage_post_no_content(tozti, db):
    assert make_call("POST", '/store/resources').status_code == 400



@pytest.mark.extensions("type")
@pytest.mark.parametrize("json", [
    {"type": TYPE,
         "attributes": {"name": "f", "email": "a@a.com"}},
    ])
def test_storage_delete_object(tozti, db, json):
    try:
        uid = add_object_get_id(json)
        c = db.count()
        make_call("DELETE", "/store/resources/{}".format(uid))
        assert c > db.count()
    except:
        assert False


def test_storage_delete_object_fail_not_uuid(tozti, db):
    assert make_call("DELETE", "/store/resources/foo").status_code == 404


def test_storage_delete_object_fail_uuid(tozti, db):
    assert make_call("DELETE", "/store/resources/00000000-0000-0000-0000-000000000000").status_code == 404


@pytest.mark.extensions("type")
@pytest.mark.parametrize("json", [
    {"type": TYPE, "attributes": {"name": "f", "email": "a@a.com"}},
    ])
def test_storage_get_object(tozti, db, json):
    try:
        uid = add_object_get_id(json)
        result = make_call("GET", "/store/resources/{}".format(uid)).json()["data"]
        expected = json
        expected["id"] = uid
        assert uid == result["id"] and json["attributes"] == result["attributes"]
    except:
        assert False


def test_storage_get_object_fail_not_uuid(tozti, db):
    assert make_call("GET", "/store/resources/foo").status_code == 404


def test_storage_get_object_fail_uuid(tozti, db):
    assert make_call("GET", "/store/resources/00000000-0000-0000-0000-000000000000").status_code == 404



@pytest.mark.extensions("type")
@pytest.mark.parametrize("json, diff, expected", [
    ({"type": TYPE, "attributes": {"name": "f", "email": "a@a.com"}}, {"name": "g"},        True),
    ({"type": TYPE, "attributes": {"name": "f", "email": "a@a.com"}}, {"email": "b@b.com"}, True),
    ({"type": TYPE, "attributes": {"name": "f", "email": "a@a.com"}}, {"email": "a"},       False),
    ({"type": TYPE, "attributes": {"name": "f", "email": "a@a.com"}}, {"bar": "a"},         False),
    ])
def test_storage_update(tozti, db, json, diff, expected):
    try:
        uid = add_object_get_id(json)
        result = make_call("PATCH", "/store/resources/{}".format(uid), json={"data": {"attributes": diff}})
        # test if the request succeeded
        if result.status_code == 200:
            theory = json
            for (k, v) in diff.items():
                if k in theory["attributes"]:
                    theory["attributes"][k] = v
            assert db_is_object(db, theory) == expected
        else:
            assert not expected
    except:
        assert False

@pytest.mark.extensions("type")
def test_storage_update_no_content(tozti, db):
    json = {"type": TYPE, "attributes": {"name": "f", "email": "a@a.com"}}
    uid = add_object_get_id(json)
    assert make_call("PATCH", "/store/resources/{}".format(uid)).status_code == 400

def test_storage_update_object_fail_not_uuid(tozti, db):
    assert make_call("PATCH", "/store/resources/foo").status_code == 404

def test_storage_update_object_fail_uuid(tozti, db):
    assert make_call("PATCH", "/store/resources/00000000-0000-0000-0000-000000000000").status_code == 400



"""
Now, tests for ressources \o/
"""
@pytest.mark.extensions("rel01")
def test_storage_rel_toone_notspecified(tozti, db):
    assert make_call("POST", "/store/resources/", json = {"type": "rel01/foo", "attributes": {"foo": "foo"}}).status_code == 404

@pytest.mark.extensions("rel01")
def test_storage_rel_toone_badrelerror(tozti, db):
    """ Test coming from a bug in tozti: at first, their was a typo in _santize_to_one
    with the presence of `BadRelData` instead of `BadRelError`
    """
    uid_bar = add_object_get_id({"type": "rel01/bar", "attributes": {"bar": "bar"}})
    assert make_call("POST", 
                    "/store/resources",
                    {"type": "rel01/foo", "attributes": {"foo": "foo"}, "relationships": {"member": uid_bar}}
                    ).status_code == 400
