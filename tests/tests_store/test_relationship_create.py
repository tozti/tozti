from tests.commons import db_contains_object, make_call, add_object_get_id
import json
import pytest
from uuid import UUID, uuid4


TYPE = "type/foo"

@pytest.mark.extensions("rel01")
def test_storage_rel_toone_notspecified(tozti, db):
    assert make_call("POST", "/store/resources", json = {"data": {"type": "rel01/foo", "body": {"foo": "foo"}}}).status_code == 400


@pytest.mark.extensions("rel02")
def test_storage_rel_tomany_notspecified(tozti, db):
    assert make_call("POST", "/store/resources", json = {"data": {"type": "rel02/foo", "body": {"foo": "foo"}}}).status_code == 400

@pytest.mark.extensions("rel01")
def test_storage_rel_toone_badrelerror(tozti, db):
    """ Test coming from a bug in tozti: at first, their was a typo in _santize_to_one
    with the presence of `BadRelData` instead of `BadRelError`.
    The test in itself doesn't mean anything, it is just here for this precise error
    """
    uid_bar = add_object_get_id({"type": "rel01/bar", "body": {"bar": "bar"}})
    assert make_call("POST", 
                    "/store/resources",
                    {"type": "rel01/foo", "body": {"foo": "foo", "member": uid_bar}}
                    ).status_code == 400

