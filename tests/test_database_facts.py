import pytest
from sqlalchemy.exc import IntegrityError
from flashcards_core.database import Fact, Tag


def test_fact_create_empty_fact(session):
    with pytest.raises(IntegrityError):
        Fact.create(session=session)


def test_fact_create_with_everything(session):
    assert Fact.create(session=session, value="fact", format="text")


def test_long_fact_repr(session):
    fact = Fact.create(
        session=session,
        value="fact fact fact fact fact fact fact fact fact "
        "fact fact fact fact fact fact fact fact ",
        format="text",
    )
    assert "<Fact 'fact fact fact fact ...' (ID: 1)>" == f"{fact}"


def test_fact_assign_and_remove_tag(session):
    fact = Fact.create(session=session, value="fact", format="text")
    tag = Tag.create(session=session, name="test-tag")
    assert len(fact.tags) == 0
    fact.assign_tag(session=session, tag_id=tag.id)
    assert len(fact.tags) == 1
    fact.remove_tag(session=session, tag_id=tag.id)
    assert len(fact.tags) == 0
