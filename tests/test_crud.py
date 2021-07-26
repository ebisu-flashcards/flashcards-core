import pytest
from conftest import StubCrud


def test_crud_get_all_empty(session):
    assert not StubCrud.get_all(session=session)


def test_crud_create_one_and_get_all(session):
    StubCrud.create(session=session, value=1000)
    assert len(StubCrud.get_all(session=session)) == 1


def test_crud_create_many_and_get_all(session):
    StubCrud.create(session=session, value=1000)
    StubCrud.create(session=session, value=3000)
    StubCrud.create(session=session, value=2000)
    assert len(StubCrud.get_all(session=session)) == 3


def test_crud_create_one_and_get_one(session):
    stub = StubCrud.create(session=session, value=5000)
    assert stub == StubCrud.get_one(session=session, object_id=stub.id)


def test_crud_create_many_and_get_one(session):
    StubCrud.create(session=session, value=7000)
    stub = StubCrud.create(session=session, value=3000)
    StubCrud.create(session=session, value=5000)
    assert stub == StubCrud.get_one(session=session, object_id=stub.id)


def test_crud_get_one_not_created(session):
    assert not StubCrud.get_one(session=session, object_id=1)


def test_crud_create_update_and_get(session):
    stub = StubCrud.create(session=session, value=5000)
    StubCrud.update(session=session, object_id=stub.id, value=2000)
    updated_stub = StubCrud.get_one(session=session, object_id=stub.id)
    assert 2000 == updated_stub.value


def test_crud_update_not_created(session):
    with pytest.raises(ValueError):
        StubCrud.update(session=session, object_id=1, value=2000)


def test_crud_create_delete_and_get(session):
    stub = StubCrud.create(session=session, value=5000)
    StubCrud.delete(session=session, object_id=stub.id)
    assert not StubCrud.get_one(session=session, object_id=stub.id)


def test_crud_delete_not_created(session):
    with pytest.raises(ValueError):
        StubCrud.delete(session=session, object_id=1)
