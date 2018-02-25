from uuid import UUID, uuid4

import pytest

from tests.commons import API, add_object_get_id, db_contains_object, make_call


@pytest.mark.extensions("rel02")
def test_storage_handle_create(tozti, db):
    type = "rel02/bar"
    uid_bar = add_object_get_id({"type": type, "body": {"bar": "bar"}})

    make_call("POST", "/store/by-handle/foo", json={'data': {'id': uid_bar}})
    result = make_call("GET", "/store/by-handle/foo")

    expected = {'data': {
        'id': uid_bar,
        'type': type,
        'href': API + '/store/resources/'+uid_bar
    }}

    assert result.json() == expected


@pytest.mark.extensions("rel02")
def test_storage_handle_create_invalid_id(tozti, db):
    uid_bar = str(UUID(int=0))

    result = make_call("POST", "/store/by-handle/foo",
                       json={'data': {'id': uid_bar}})
    assert result.status_code == 404
    assert result.json()['errors'][0]['code'] == 'NO_RESOURCE'

    result = make_call("GET", "/store/by-handle/foo")
    assert result.status_code == 404
    assert result.json()['errors'][0]['code'] == 'NO_HANDLE'


@pytest.mark.extensions("rel02")
def test_storage_handle_query_invalid_handle(tozti, db):
    result = make_call("GET", "/store/by-handle/foo")
    assert result.status_code == 404
    assert result.json()['errors'][0]['code'] == 'NO_HANDLE'


@pytest.mark.extensions("rel02")
def test_storage_handle_replace_existing(tozti, db):
    type = "rel02/bar"

    for _ in range(2):
        uid_bar = add_object_get_id({"type": type, "body": {"bar": "bar"}})
        make_call("POST", "/store/by-handle/foo",
                  json={'data': {'id': uid_bar}})
        result = make_call("GET", "/store/by-handle/foo")
        assert result.json()['data']['id'] == uid_bar

@pytest.mark.extensions("rel02")
def test_storage_handle_create_invalid_json(tozti, db):
    result = make_call("POST", "/store/by-handle/foo", json={'data': 'something invalid'})
    assert result.json()['errors'][0]['code'] == 'BAD_DATA'

    result = make_call("GET", "/store/by-handle/foo")
    assert result.json()['errors'][0]['code'] == 'NO_HANDLE'

@pytest.mark.extensions("rel02")
def test_storage_handle_delete(tozti, db):
    type = "rel02/bar"
    uid_bar = add_object_get_id({"type": type, "body": {"bar": "bar"}})

    make_call("POST", "/store/by-handle/foo", json={'data': {'id': uid_bar}})
    
    result = make_call("DELETE", "/store/by-handle/foo")
    assert result.json() == {}

    result = make_call("GET", "/store/by-handle/foo")
    assert result.status_code == 404
    assert result.json()['errors'][0]['code'] == 'NO_HANDLE'

@pytest.mark.extensions("rel02")
def test_storage_handle_delete_invalid(tozti, db):
    result = make_call("DELETE", "/store/by-handle/foo")
    
    assert result.status_code == 404
    assert result.json()['errors'][0]['code'] == 'NO_HANDLE'