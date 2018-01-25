from commons import launch_tozti, stop_tozti
import json
from requests import get, post, put, patch, delete
import requests
from pymongo import MongoClient
import pytest


API = 'http://127.0.0.1:8080/api'
USER_TYPE = "http://127.0.0.1:8080/static/core/types/user.json"


@pytest.fixture(scope="module")
def tozti(request):
    tozti = launch_tozti()
    if tozti is None:
        assert(False)

    yield tozti

    def end():
        stop_tozti(tozti)
    request.addfinalizer(end)

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

@pytest.mark.parametrize("json, expected", [
    ({"type": USER_TYPE,
         "attributes": {"name": "f", "email": "a@a.com", "login": "bjr"}}, True),
    ({"type": USER_TYPE,
         "atxtributes": {"name": "f", "email": "a@a.com", "login": "bjr"}}, False)
    ])
def test_storage_post_request(tozti, db, json, expected):
    ret_val = check_call("POST", '/store/resources', json={"data": json})
    if not ret_val and expected:
        assert(True)
    if db.count() != 1:
        assert(not expected)
    for obj in db.find():
        if obj["attrs"] != json["attributes"]:
            assert(not expected)

@pytest.mark.parametrize("json", [
    {"type": USER_TYPE,
         "attributes": {"name": "f", "email": "a@a.com", "login": "bjr"}},
    ])
def test_storage_delete_object(tozti, db, json):
    try:
        ret_val = make_call("POST", '/store/resources', json={"data": json}).json()
        uid = ret_val['data']['id']
        c = db.count()
        make_call("DELETE", "/store/resources/{}".format(uid))
        assert(c > db.count())
    except:
        assert(False)

def test_storage_delete_object_fail_not_uuid(tozti, db):
    assert make_call("DELETE", "/store/resources/{}".format("foo"), json=None).status_code == 404

def test_storage_delete_object_fail_uuid(tozti, db):
    assert make_call("DELETE", "/store/resources/00000000-0000-0000-0000-000000000000").status_code == 404

