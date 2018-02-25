from tests.commons import db_contains_object, make_call, add_object_get_id
import json
import pytest
from uuid import UUID, uuid4

# using post on a relationship
@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_post_empty(tozti, db):
    uid_foo = add_object_get_id({"type": "rel02/foo", "body": {"foo": "foo", "members": {"data": []}}})
    result = make_call("POST", "/store/resources/{}/members".format(uid_foo), json={"data": []})
    assert result.status_code == 200

@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_post_wrong_type(tozti, db):
    bar = {"body": {"bar": "bar"}}
    uid_bar = add_object_get_id({"type": "rel02/bar", "body": {"bar": "bar"}})
    uid_foo = add_object_get_id({"type": "rel02/foo", "body": {"foo": "foo", "members": {"data": [{"id": uid_bar}]}}})

    result = make_call("POST", "/store/resources/{}/members".format(uid_foo), json={"data": [{'id': uid_foo, 'type': 'rel02/bar'}]})
    assert result.status_code == 400

@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_post_valid(tozti, db):
    bar = {"body": {"bar": "bar"}}
    uid_bar = add_object_get_id({"type": "rel02/bar", "body": {"bar": "bar"}})
    uid_bar2 = add_object_get_id({"type": "rel02/bar", "body": {"bar": "bar"}})
    uid_foo = add_object_get_id({"type": "rel02/foo", "body": {"foo": "foo", "members": {"data": [{"id": uid_bar}]}}})

    result = make_call("POST", "/store/resources/{}/members".format(uid_foo), json={"data": [{'id': uid_bar2, 'type': 'rel02/bar'}]})
    assert result.status_code == 200

    foo = {"body": {"foo": "foo", "members": [{'id': UUID(uid_bar), 'type': 'rel02/bar'}, {'id': UUID(uid_bar2), 'type': 'rel02/bar'}]}}
    assert db_contains_object(db, foo)

@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_post_incorrect_format(tozti, db):
    uid_foo = add_object_get_id({"type": "rel02/foo", "body": {"foo": "foo", "members": {"data": []}}})
    result = make_call("POST", "/store/resources/{}/members".format(uid_foo), json={"foo": "bar"})
    assert result.status_code == 400

@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_post_nonexistingrel(tozti, db):
    uid_foo = add_object_get_id({"type": "rel02/foo", "body": {"foo": "foo", "members": {"data": []}}})
    # bug here, should return 404
    result = make_call("POST", "/store/resources/{}/foo".format(uid_foo), json={"data": {}})
    assert result.status_code == 400

@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_post_nonexistingres(tozti, db):
    result = make_call("POST", "/store/resources/bar/members", json={"foo": "bar"})
    assert result.status_code == 404

# now, to one rel
@pytest.mark.extensions("rel01")
def test_storage_rel_toone_post_valid(tozti, db):
    bar = {"body": {"bar": "bar"}}
    uid_bar = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    uid_bar2 = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    uid_foo = add_object_get_id({"type": "rel01/foo", "body": {"foo": "foo", "member": {"data": {"id": uid_bar}}}})

    result = make_call("POST", "/store/resources/{}/member".format(uid_foo), json={"data": {'id': uid_bar2, 'type': 'rel01/bar'}})
    assert result.status_code == 400

    foo = {"body": {"foo": "foo", "member": {'id': UUID(uid_bar), 'type': 'rel01/bar'}}}
    assert db_contains_object(db, foo)

@pytest.mark.extensions("rel01")
def test_storage_rel_toone_post_invalid_type(tozti, db):
    bar = {"body": {"bar": "bar"}}
    uid_bar = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    uid_foo = add_object_get_id({"type": "rel01/foo", "body": {"foo": "foo", "member": {"data": {"id": uid_bar}}}})

    result = make_call("POST", "/store/resources/{}/member".format(uid_foo), json={"data": [{'id': uid_bar, 'type': 'rel01/bar'}]})
    assert result.status_code == 400
