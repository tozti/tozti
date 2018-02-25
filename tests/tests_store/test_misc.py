from tests.commons import db_contains_object, make_call, add_object_get_id
import json
import pytest
from uuid import UUID, uuid4

def test_bad_json_type(tozti):
    assert make_call("POST", "/store/resources", json={'data':{}}, content_type = "oifzeh").status_code == 406
