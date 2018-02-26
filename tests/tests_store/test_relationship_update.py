from tests.commons import db_contains_object, make_call, add_object_get_id
import json
import pytest
from uuid import UUID, uuid4


TYPE = "type/foo"

# using patch on a ressource
@pytest.mark.extensions("rel01")
def test_storage_rel_toone_post(tozti, db):
    bar = {"body": {"bar": "bar"}}
    uid_bar = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    foo = {"body": {"foo": "foo", "member": {"id": UUID(uid_bar), "type": "rel01/bar"}}}
    uid_foo = add_object_get_id({"type": "rel01/foo", "body": {"foo": "foo", "member": {"data": {"id": uid_bar}}}})
    if db.count() == 2:
        assert db_contains_object(db, bar) and db_contains_object(db, foo)
    else:
        assert False
@pytest.mark.extensions("rel01")
def test_storage_rel_toone_owner_patch_empty(tozti, db):
    bar = {"body": {"bar": "bar"}}
    uid_bar = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    uid_foo = add_object_get_id({"type": "rel01/foo", "body": {"foo": "foo", "member": {"data": {"id": uid_bar}}}})

    result = make_call("PATCH", "/store/resources/{}".format(uid_foo), json={"data": {"body": {}}})
    assert result.status_code == 200

@pytest.mark.extensions("rel01")
def test_storage_rel_toone_owner_patch(tozti, db):
    uid_bar = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    uid_bar2 = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    uid_foo = add_object_get_id({"type": "rel01/foo", "body": {"foo": "foo", "member": {"data": {"id": uid_bar}}}})

    foo = {"body": {"foo": "foo", "member": {"id": UUID(uid_bar), "type": "rel01/bar"}}}
    assert db_contains_object(db, foo)

    result = make_call("PATCH", "/store/resources/{}".format(uid_foo), json={"data": {"body": {"member": {"data": {"id": uid_bar2}}}}})
    assert result.status_code == 200

    foo = {"body": {"foo": "foo", "member": {"id": UUID(uid_bar2), "type": "rel01/bar"}}}
    assert db_contains_object(db, foo)


@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_owner_patch(tozti, db):
    bar = {"body": {"bar": "bar"}}
    uid_bar = add_object_get_id({"type": "rel02/bar", "body": {"bar": "bar"}})
    bar2 = {"body": {"bar": "bar"}}
    uid_bar2 = add_object_get_id({"type": "rel02/bar", "body": {"bar": "bar"}})
    uid_foo = add_object_get_id({"type": "rel02/foo", "body": {"foo": "foo", "members": {"data": [{"id": uid_bar}]}}})

    foo = {"body": {"foo": "foo", "members": [{"id": UUID(uid_bar), "type": "rel02/bar"}]}}
    assert db_contains_object(db, foo)

    result = make_call("PATCH", "/store/resources/{}".format(uid_foo), json={"data": {"body": {"members": {"data": [{"id": uid_bar2}]}}}})
    assert result.status_code == 200

    foo = {"body": {"foo": "foo", "members": [{"id": UUID(uid_bar2), "type": "rel02/bar"}]}}
    assert db_contains_object(db, foo)

@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_owner_patch_empty(tozti, db):
    bar = {"body": {"bar": "bar"}}
    uid_bar = add_object_get_id({"type": "rel02/bar", "body": {"bar": "bar"}})
    uid_foo = add_object_get_id({"type": "rel02/foo", "body": {"foo": "foo", "members": {"data": [{"id": uid_bar}]}}})

    foo = {"body": {"foo": "foo", "members": [{"id": UUID(uid_bar), "type": "rel02/bar"}]}}
    assert db_contains_object(db, foo)

    result = make_call("PATCH", "/store/resources/{}".format(uid_foo), json={"data": {"body": {"members": {"data": []}}}})
    assert result.status_code == 200

    foo = {"body": {"foo": "foo", "members": []}}
    assert db_contains_object(db, foo)

