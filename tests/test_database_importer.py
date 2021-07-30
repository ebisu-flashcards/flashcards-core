# import json
import pytest

# from freezegun import freeze_time

from flashcards_core.database import Deck  # , Card, Fact, Review, Tag
from flashcards_core.database.importer import import_from_dict  # , import_from_json


def test_import(session):
    deck = {
        "decks": {
            "d852834b-ff4f-4032-9e83-c46cb9989861": {
                "algorithm": "random",
                "state": {},
                "description": "A long description for deck",
                "name": "Test",
                "parameters": {},
            }
        },
        "cards": {
            "d852834b-ff4f-4032-9e83-c46cb9989862": {
                "deck_id": "d852834b-ff4f-4032-9e83-c46cb9989861",
                "question_id": "d852834b-ff4f-4032-9e83-c46cb9989863",
                "answer_id": "d852834b-ff4f-4032-9e83-c46cb9989864",
            }
        },
        "facts": {
            "d852834b-ff4f-4032-9e83-c46cb9989863": {
                "format": "plaintext",
                "value": "a question",
            },
            "d852834b-ff4f-4032-9e83-c46cb9989864": {
                "format": "plaintext",
                "value": "an answer",
            },
        },
    }
    import_from_dict(session=session, hierarchy=deck)
    assert (
        str(Deck.get_all(session=session)[0])
        == "<Deck 'Test' (ID: d852834b-ff4f-4032-9e83-c46cb9989861)>"
    )


def test_import_twice_same_object(session):
    deck = {
        "decks": {
            "d852834b-ff4f-4032-9e83-c46cb9989861": {
                "algorithm": "random",
                "state": {},
                "description": "A long description for deck",
                "name": "Test",
                "parameters": {},
            }
        }
    }
    import_from_dict(session=session, hierarchy=deck)
    import_from_dict(session=session, hierarchy=deck)


def test_import_wrong_tablename(session):
    deck = {
        "wrong": {
            "d852834b-ff4f-4032-9e83-c46cb9989861": {
                "algorithm": "random",
                "state": {},
                "description": "A long description for deck",
                "name": "Test",
                "parameters": {},
            }
        }
    }
    with pytest.raises(ValueError):
        import_from_dict(session=session, hierarchy=deck)
