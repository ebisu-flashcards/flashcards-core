# import json
import pytest
import datetime
from sqlalchemy.exc import IntegrityError

from flashcards_core.database import Deck, Card, Fact, Review, Tag
from flashcards_core.database.importer import import_from_dict  # , import_from_json


def test_import_one_object(session):
    hierarchy = {
        "decks": {
            "d852834bff4f40329e83c46cb9989861": {
                "algorithm": "random",
                "state": {},
                "description": "A long description for deck",
                "name": "Test",
                "parameters": {},
            }
        }
    }
    import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)
    assert len(Deck.get_all(session=session)) == 1
    assert Deck.get_all(session=session)[0].id.hex == "d852834bff4f40329e83c46cb9989861"


def test_import_one_association_table(session):
    hierarchy = {
        "facttags": [
            ("d852834bff4f40329e83c46cb9989863", "d852834bff4f40329e83c46cb9989867")
        ],
    }
    import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)


def test_import_twice_same_object(session):
    hierarchy = {
        "decks": {
            "d852834bff4f40329e83c46cb9989861": {
                "algorithm": "random",
                "state": {},
                "description": "A long description for deck",
                "name": "Test",
                "parameters": {},
            }
        }
    }
    import_from_dict(session=session, hierarchy=hierarchy)
    import_from_dict(session=session, hierarchy=hierarchy)
    assert len(Deck.get_all(session=session)) == 1
    assert Deck.get_all(session=session)[0].id.hex == "d852834bff4f40329e83c46cb9989861"
    with pytest.raises(IntegrityError):
        import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)


def test_import_twice_same_association_table(session):
    hierarchy = {
        "facttags": [
            ("d852834bff4f40329e83c46cb9989863", "d852834bff4f40329e83c46cb9989867")
        ],
    }
    import_from_dict(session=session, hierarchy=hierarchy)
    import_from_dict(session=session, hierarchy=hierarchy)
    with pytest.raises(IntegrityError):
        import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)


def test_import_wrong_tablename(session):
    hierarchy = {
        "wrong": {
            "d852834bff4f40329e83c46cb9989861": {
                "algorithm": "random",
                "state": {},
                "description": "A long description for deck",
                "name": "Test",
                "parameters": {},
            }
        }
    }
    import_from_dict(session=session, hierarchy=hierarchy)
    with pytest.raises(ValueError):
        import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)


def test_import_malformed_object(session):
    hierarchy = {"wrong": "value"}
    import_from_dict(session=session, hierarchy=hierarchy)
    with pytest.raises(ValueError):
        import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)


def test_import_full_hierarchy(session):
    hierarchy = {
        "decks": {
            "d852834bff4f40329e83c46cb9989861": {
                "name": "Test",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {
            "d852834bff4f40329e83c46cb9989862": {
                "deck_id": "d852834bff4f40329e83c46cb9989861",
                "question_id": "d852834bff4f40329e83c46cb9989863",
                "answer_id": "d852834bff4f40329e83c46cb9989864",
            }
        },
        "facts": {
            "d852834bff4f40329e83c46cb9989863": {"format": "text", "value": "question"},
            "d852834bff4f40329e83c46cb9989864": {"format": "text", "value": "answer"},
        },
        "reviews": {
            "d852834bff4f40329e83c46cb9989865": {
                "algorithm": "random",
                "card_id": "d852834bff4f40329e83c46cb9989862",
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "1",
            },
            "d852834bff4f40329e83c46cb9989866": {
                "algorithm": "random",
                "card_id": "d852834bff4f40329e83c46cb9989862",
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "0",
            },
        },
        "tags": {
            "d852834bff4f40329e83c46cb9989867": {"name": "testtag1"},
            "d852834bff4f40329e83c46cb9989868": {"name": "testtag2"},
        },
        "facttags": [
            ("d852834bff4f40329e83c46cb9989863", "d852834bff4f40329e83c46cb9989867")
        ],
        "cardtags": [
            ("d852834bff4f40329e83c46cb9989862", "d852834bff4f40329e83c46cb9989868")
        ],
        "decktags": [
            ("d852834bff4f40329e83c46cb9989861", "d852834bff4f40329e83c46cb9989867")
        ],
    }
    import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)

    assert Deck.get_all(session=session)[0].id.hex == "d852834bff4f40329e83c46cb9989861"
    assert Card.get_all(session=session)[0].id.hex == "d852834bff4f40329e83c46cb9989862"
    assert Fact.get_all(session=session)[0].id.hex == "d852834bff4f40329e83c46cb9989863"
    assert Fact.get_all(session=session)[1].id.hex == "d852834bff4f40329e83c46cb9989864"
    assert (
        Review.get_all(session=session)[0].id.hex == "d852834bff4f40329e83c46cb9989865"
    )
    assert (
        Review.get_all(session=session)[1].id.hex == "d852834bff4f40329e83c46cb9989866"
    )
    assert Tag.get_all(session=session)[0].id.hex == "d852834bff4f40329e83c46cb9989867"
    assert Tag.get_all(session=session)[1].id.hex == "d852834bff4f40329e83c46cb9989868"

    assert ["d852834bff4f40329e83c46cb9989867"] == [
        tag.id.hex for tag in Deck.get_all(session=session)[0].tags
    ]
    assert ["d852834bff4f40329e83c46cb9989868"] == [
        tag.id.hex for tag in Card.get_all(session=session)[0].tags
    ]
    assert ["d852834bff4f40329e83c46cb9989867"] == [
        tag.id.hex for tag in Fact.get_all(session=session)[0].tags
    ]
