# import json
import pytest
import datetime
from uuid import UUID
from sqlalchemy.exc import IntegrityError

from flashcards_core.database import (
    Deck,
    Card,
    Fact,
    Review,
    Tag,
    DeckTag,
    CardTag,
    FactTag,
)
from flashcards_core.database.importer import import_from_dict  # , import_from_json
from flashcards_core.database.exporter import export_to_dict


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


def test_import_and_export_full_hierarchy(session):
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
                "deck_id": UUID("d852834bff4f40329e83c46cb9989861"),
                "question_id": UUID("d852834bff4f40329e83c46cb9989863"),
                "answer_id": UUID("d852834bff4f40329e83c46cb9989864"),
            }
        },
        "facts": {
            "d852834bff4f40329e83c46cb9989863": {"format": "text", "value": "question"},
            "d852834bff4f40329e83c46cb9989864": {"format": "text", "value": "answer"},
        },
        "reviews": {
            "d852834bff4f40329e83c46cb9989865": {
                "algorithm": "random",
                "card_id": UUID("d852834bff4f40329e83c46cb9989862"),
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "1",
            },
            "d852834bff4f40329e83c46cb9989866": {
                "algorithm": "random",
                "card_id": UUID("d852834bff4f40329e83c46cb9989862"),
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "0",
            },
        },
        "tags": {
            "d852834bff4f40329e83c46cb9989867": {"name": "testtag1"},
            "d852834bff4f40329e83c46cb9989868": {"name": "testtag2"},
        },
        "facttags": {
            (
                UUID("d852834bff4f40329e83c46cb9989863"),
                UUID("d852834bff4f40329e83c46cb9989867"),
            )
        },
        "cardtags": {
            (
                UUID("d852834bff4f40329e83c46cb9989862"),
                UUID("d852834bff4f40329e83c46cb9989868"),
            )
        },
        "decktags": {
            (
                UUID("d852834bff4f40329e83c46cb9989861"),
                UUID("d852834bff4f40329e83c46cb9989867"),
            )
        },
    }

    # Import and re-export
    import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)
    deck = Deck.get_all(session=session)[0]
    new_hierarchy = export_to_dict(session=session, objects_to_export=[deck])

    assert hierarchy == new_hierarchy


def test_export_and_import_full_hierarchy(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for deck",
        algorithm="random",
    )
    question = Fact.create(session=session, value="question", format="text")
    answer = Fact.create(session=session, value="answer", format="text")
    card = Card.create(
        session=session,
        deck_id=deck.id.hex,
        question_id=question.id.hex,
        answer_id=answer.id.hex,
    )
    review1 = Review.create(
        session=session, result=True, algorithm="random", card_id=card.id.hex
    )
    review2 = Review.create(
        session=session, result=False, algorithm="random", card_id=card.id.hex
    )
    tag1 = Tag.create(session=session, name="test-tag-1")
    tag2 = Tag.create(session=session, name="test-tag-2")
    deck.assign_tag(session=session, tag_id=tag1.id.hex)
    card.assign_tag(session=session, tag_id=tag2.id.hex)
    question.assign_tag(session=session, tag_id=tag1.id.hex)

    # Export and re-import
    hierarchy = export_to_dict(session=session, objects_to_export=[deck])

    session.query(Deck).delete()
    session.query(Card).delete()
    session.query(Fact).delete()
    session.query(Review).delete()
    session.query(Tag).delete()
    session.query(DeckTag).delete()
    session.query(CardTag).delete()
    session.query(FactTag).delete()
    assert not Deck.get_all(session=session)
    assert not Card.get_all(session=session)
    assert not Fact.get_all(session=session)
    assert not Review.get_all(session=session)
    assert not Tag.get_all(session=session)

    import_from_dict(session=session, hierarchy=hierarchy, stop_on_error=True)

    assert Deck.get_one(session=session, object_id=deck.id)
    assert len(Deck.get_one(session=session, object_id=deck.id).cards) == 1
    assert len(Deck.get_one(session=session, object_id=deck.id).tags) == 1

    assert Card.get_one(session=session, object_id=card.id)
    assert len(Card.get_one(session=session, object_id=card.id).tags) == 1
    assert len(Card.get_one(session=session, object_id=card.id).reviews) == 2

    assert Fact.get_one(session=session, object_id=question.id)
    assert len(Fact.get_one(session=session, object_id=question.id).tags) == 1

    assert Fact.get_one(session=session, object_id=answer.id)
    assert len(Fact.get_one(session=session, object_id=answer.id).tags) == 0

    assert Review.get_one(session=session, object_id=review1.id)
    assert Review.get_one(session=session, object_id=review2.id)
    assert Tag.get_one(session=session, object_id=tag1.id)
    assert Tag.get_one(session=session, object_id=tag2.id)
