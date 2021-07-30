import json
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


def test_export_to_dict_no_objects(session):
    hierarchy = export_to_dict(session=session, objects_to_export=[])
    assert hierarchy == {}


def test_export_to_dict_objects_are_None(session):
    hierarchy = export_to_dict(session=session, objects_to_export=[None, None])
    assert hierarchy == {}


def test_export_to_dict_broken_references(session):
    card = Card.create(session=session, deck_id=1, question_id=1, answer_id=2)
    hierarchy = export_to_dict(session=session, objects_to_export=[card])
    assert hierarchy == {"cards": {1: {"deck_id": 1, "question_id": 1, "answer_id": 2}}}


def test_export_to_dict_one_object_no_list(session):
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


def test_export_to_dict_same_object_twice(session):
    deck = Deck.create(
        session=session,
        name="Test",
        description="A long description for deck",
        algorithm="random",
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[deck, deck])
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


def test_export_to_dict_two_objects_of_same_type(session):
    deck1 = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    deck2 = Deck.create(
        session=session,
        name="Test-2",
        description="A long description for deck",
        algorithm="random",
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[deck1, deck2])
    assert hierarchy == {
        "decks": {
            1: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            },
            2: {
                "name": "Test-2",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            },
        }
    }


def test_export_to_dict_two_different_unrelated_objects(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    fact = Fact.create(
        session=session,
        value="a fact",
        format="plaintext",
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[deck, fact])
    assert hierarchy == {
        "decks": {
            1: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "facts": {1: {"value": "a fact", "format": "plaintext"}},
    }


def test_export_to_dict_two_related_objects_deck_first(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=1,
        answer_id=2,
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[deck, card])
    assert hierarchy == {
        "decks": {
            1: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {
            1: {
                "deck_id": 1,
                "question_id": 1,
                "answer_id": 2,
            }
        },
    }


def test_export_to_dict_two_related_objects_card_first(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=1,
        answer_id=2,
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[card, deck])
    assert hierarchy == {
        "decks": {
            1: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {
            1: {
                "deck_id": 1,
                "question_id": 1,
                "answer_id": 2,
            }
        },
    }


def test_export_to_dict_card_dont_pull_deck(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=1,
        answer_id=2,
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[card])
    assert hierarchy == {
        "cards": {
            1: {
                "deck_id": 1,
                "question_id": 1,
                "answer_id": 2,
            }
        }
    }


def test_export_to_dict_card_pull_deck(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=1,
        answer_id=2,
    )
    hierarchy = export_to_dict(
        session=session, objects_to_export=[card], exclude_fields={}
    )
    assert hierarchy == {
        "decks": {
            1: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {
            1: {
                "deck_id": 1,
                "question_id": 1,
                "answer_id": 2,
            }
        },
    }


def test_export_to_dict_card_pull_nothing(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    question = Fact.create(session=session, value="question", format="text")
    answer = Fact.create(session=session, value="answer", format="text")
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=question.id,
        answer_id=answer.id,
    )
    hierarchy = export_to_dict(
        session=session,
        objects_to_export=[card],
        exclude_fields={"cards": ["deck", "question", "answer"]},
    )
    assert hierarchy == {
        "cards": {
            1: {
                "deck_id": 1,
                "question_id": 1,
                "answer_id": 2,
            }
        }
    }


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
    Review.create(session=session, result=True, algorithm="random", card_id=card.id)
    Review.create(session=session, result=False, algorithm="random", card_id=card.id)
    tag1 = Tag.create(session=session, name="test-tag-1")
    tag2 = Tag.create(session=session, name="test-tag-2")

    deck.assign_tag(session=session, tag_id=tag1.id)
    card.assign_tag(session=session, tag_id=tag2.id)

    hierarchy = export_to_dict(session=session, objects_to_export=[card, deck])
    assert hierarchy == {
        "decks": {
            1: {
                "name": "Test",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {1: {"deck_id": 1, "question_id": 1, "answer_id": 2}},
        "facts": {
            1: {"format": "text", "value": "question"},
            2: {"format": "text", "value": "answer"},
        },
        "reviews": {
            1: {
                "algorithm": "random",
                "card_id": 1,
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "1",
            },
            2: {
                "algorithm": "random",
                "card_id": 1,
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "0",
            },
        },
        "tags": {2: {"name": "test-tag-2"}, 1: {"name": "test-tag-1"}},
        "cardtags": {1: {"card_id": 1, "tag_id": 2}},
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
