import json
import pytest
import datetime
from freezegun import freeze_time

from flashcards_core.database import (
    Deck,
    Card,
    Fact,
    Review,
    Tag,
    export_to_dict,
    export_to_json,
)


def test_export_to_dict_one_object_no_list(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for deck",
        algorithm="random",
    )
    with pytest.raises(ValueError):
        export_to_dict(session=session, objects_to_export=deck)


def test_export_to_dict_one_object_in_list(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for deck",
        algorithm="random",
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[deck])
    assert hierarchy == {
        "decks": {
            1: {
                "name": "Test",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        }
    }


def test_export_to_dict_broken_references(session):
    card = Card.create(session=session, deck_id=1, question_id=1, answer_id=2)
    hierarchy = export_to_dict(session=session, objects_to_export=[card])
    assert hierarchy == {"cards": {1: {"deck_id": 1, "question_id": 1, "answer_id": 2}}}


@freeze_time("2021-01-01 12:00:00")
def test_export_to_dict_full_hierarchy(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for deck",
        algorithm="random",
    )
    question = Fact.create(session=session, value="question", format="text")
    answer = Fact.create(session=session, value="answer", format="text")
    card = Card.create(
        session=session, deck_id=deck.id, question_id=question.id, answer_id=answer.id
    )
    Review.create(session=session, result="review", algorithm="random", card_id=card.id)
    tag1 = Tag.create(session=session, name="test-tag-1")
    tag2 = Tag.create(session=session, name="test-tag-2")

    deck.assign_tag(session=session, tag_id=tag1.id)
    card.assign_tag(session=session, tag_id=tag2.id)

    hierarchy = export_to_dict(session=session, objects_to_export=[card, deck])
    assert hierarchy == {
        "cards": {1: {"deck_id": 1, "question_id": 1, "answer_id": 2}},
        "reviews": {
            1: {
                "algorithm": "random",
                "card_id": 1,
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "review",
            }
        },
        "tags": {2: {"name": "test-tag-2"}, 1: {"name": "test-tag-1"}},
        "cardtags": {1: {"card_id": 1, "tag_id": 2}},
        "decks": {
            1: {
                "name": "Test",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "decktags": {1: {"deck_id": 1, "tag_id": 1}},
    }


def test_export_to_json(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for deck",
        algorithm="random",
    )
    hierarchy = export_to_json(
        session=session, objects_to_export=[deck], sort_keys=True
    )
    assert hierarchy == json.dumps(
        {
            "decks": {
                "1": {
                    "name": "Test",
                    "description": "A long description for deck",
                    "algorithm": "random",
                    "state": {},
                    "parameters": {},
                }
            }
        },
        sort_keys=True,
    )
