from tests.commons import db_contains_object, make_call, add_object_get_id
import json
import pytest
from uuid import UUID, uuid4


TYPE = "type/foo"


@pytest.mark.extensions("type")
def test_storage_update_empty(tozti, db):
    uid = add_object_get_id({"type": TYPE, "body": {"name": "f", "email": "a@a.com"}})
    assert (False) # because server error
    assert make_call("PATCH", "/store/resources/{}".format(uid), json={"data":{"body": {}}}).status_code == 500


@pytest.mark.extensions("type")
def test_storage_update_invalid_entry(tozti, db):
    uid = add_object_get_id({"type": TYPE, "body": {"name": "f", "email": "a@a.com"}})
    assert make_call("PATCH", "/store/resources/{}".format(uid), json={"data":{"body": {"bar": "a"}}}).status_code == 400

@pytest.mark.extensions("type")
def test_storage_update_invalid_entry_type(tozti, db):
    uid = add_object_get_id({"type": TYPE, "body": {"name": "f", "email": "a@a.com"}})
    assert make_call("PATCH", "/store/resources/{}".format(uid), json={"data":{"body": {"email": "a"}}}).status_code == 400


@pytest.mark.extensions("type")
def test_storage_update_valid(tozti, db):
    uid = add_object_get_id({"type": TYPE, "body": {"name": "f", "email": "a@a.com"}})
    theory = {"type": TYPE, "body": {"name": "g", "email": "a@a.com"}}
    assert make_call("PATCH", "/store/resources/{}".format(uid),
                    json={"data": {"body": {"name": "g"}}}).status_code == 200
    assert db.count() == 1
    assert db_contains_object(db, theory)

@pytest.mark.extensions("type")
def test_storage_update_no_content(tozti, db):
    json = {"type": TYPE, "body": {"name": "f", "email": "a@a.com"}}
    uid = add_object_get_id(json)
    assert make_call("PATCH", "/store/resources/{}".format(uid)).status_code == 400

def test_storage_update_object_fail_not_uuid(tozti, db):
    assert make_call("PATCH", "/store/resources/foo").status_code == 404

def test_storage_update_object_fail_uuid(tozti, db):
    assert make_call("PATCH", "/store/resources/00000000-0000-0000-0000-000000000000").status_code == 400
