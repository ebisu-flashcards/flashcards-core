import json
import datetime
from uuid import uuid4
from freezegun import freeze_time

from flashcards_core.database import Deck, Card, Fact, Review, Tag
from flashcards_core.database.exporter import (
    export_to_dict,
    export_to_json,
    serialize_uuids,
)


def test_export_to_dict_no_objects(session):
    hierarchy = export_to_dict(session=session, objects_to_export=[])
    assert hierarchy == {}


def test_export_to_dict_objects_are_None(session):
    hierarchy = export_to_dict(session=session, objects_to_export=[None, None])
    assert hierarchy == {}


def test_export_to_dict_broken_references(session):
    id1 = uuid4()
    id2 = uuid4()
    id3 = uuid4()
    card = Card.create(session=session, deck_id=id1, question_id=id2, answer_id=id3)
    hierarchy = export_to_dict(session=session, objects_to_export=[card])
    assert hierarchy == {
        "cards": {card.id: {"deck_id": id1, "question_id": id2, "answer_id": id3}}
    }


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
            deck.id: {
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
            deck.id: {
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
            deck.id: {
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
            deck1.id: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            },
            deck2.id: {
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
            deck.id: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "facts": {fact.id: {"value": "a fact", "format": "plaintext"}},
    }


def test_export_to_dict_two_related_objects_deck_first(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    question = Fact.create(
        session=session,
        value="a question",
        format="plaintext",
    )
    answer = Fact.create(
        session=session,
        value="an answer",
        format="plaintext",
    )
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=question.id,
        answer_id=answer.id,
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[deck, card])
    assert hierarchy == {
        "decks": {
            deck.id: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {
            card.id: {
                "deck_id": deck.id,
                "question_id": question.id,
                "answer_id": answer.id,
            }
        },
        "facts": {
            answer.id: {"format": "plaintext", "value": "an answer"},
            question.id: {"format": "plaintext", "value": "a question"},
        },
    }


def test_export_to_dict_two_related_objects_card_first(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    question = Fact.create(
        session=session,
        value="a question",
        format="plaintext",
    )
    answer = Fact.create(
        session=session,
        value="an answer",
        format="plaintext",
    )
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=question.id,
        answer_id=answer.id,
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[card, deck])
    assert hierarchy == {
        "decks": {
            deck.id: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {
            card.id: {
                "deck_id": deck.id,
                "question_id": question.id,
                "answer_id": answer.id,
            }
        },
        "facts": {
            question.id: {"format": "plaintext", "value": "a question"},
            answer.id: {"format": "plaintext", "value": "an answer"},
        },
    }


def test_export_to_dict_card_dont_pull_deck(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    question = Fact.create(
        session=session,
        value="a question",
        format="plaintext",
    )
    answer = Fact.create(
        session=session,
        value="an answer",
        format="plaintext",
    )
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=question.id,
        answer_id=answer.id,
    )
    hierarchy = export_to_dict(session=session, objects_to_export=[card])
    assert hierarchy == {
        "cards": {
            card.id: {
                "deck_id": deck.id,
                "question_id": question.id,
                "answer_id": answer.id,
            }
        },
        "facts": {
            question.id: {"format": "plaintext", "value": "a question"},
            answer.id: {"format": "plaintext", "value": "an answer"},
        },
    }


def test_export_to_dict_card_pull_deck(session):
    deck = Deck.create(
        session=session,
        name="Test-1",
        description="A long description for deck",
        algorithm="random",
    )
    question = Fact.create(
        session=session,
        value="a question",
        format="plaintext",
    )
    answer = Fact.create(
        session=session,
        value="an answer",
        format="plaintext",
    )
    card = Card.create(
        session=session,
        deck_id=deck.id,
        question_id=question.id,
        answer_id=answer.id,
    )
    hierarchy = export_to_dict(
        session=session, objects_to_export=[card], exclude_fields={}
    )
    assert hierarchy == {
        "decks": {
            deck.id: {
                "name": "Test-1",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {
            card.id: {
                "deck_id": deck.id,
                "question_id": question.id,
                "answer_id": answer.id,
            }
        },
        "facts": {
            question.id: {"format": "plaintext", "value": "a question"},
            answer.id: {"format": "plaintext", "value": "an answer"},
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
            card.id: {
                "deck_id": deck.id,
                "question_id": question.id,
                "answer_id": answer.id,
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
    review1 = Review.create(
        session=session, result=True, algorithm="random", card_id=card.id
    )
    review2 = Review.create(
        session=session, result=False, algorithm="random", card_id=card.id
    )
    tag1 = Tag.create(session=session, name="test-tag-1")
    tag2 = Tag.create(session=session, name="test-tag-2")

    decktag = deck.assign_tag(session=session, tag_id=tag1.id)
    decktag_id = decktag.inserted_primary_key[0]
    cardtag = card.assign_tag(session=session, tag_id=tag2.id)
    cardtag_id = cardtag.inserted_primary_key[0]

    hierarchy = export_to_dict(session=session, objects_to_export=[card, deck])

    assert hierarchy == {
        "decks": {
            deck.id: {
                "name": "Test",
                "description": "A long description for deck",
                "algorithm": "random",
                "state": {},
                "parameters": {},
            }
        },
        "cards": {
            card.id: {
                "deck_id": deck.id,
                "question_id": question.id,
                "answer_id": answer.id,
            }
        },
        "facts": {
            question.id: {"format": "text", "value": "question"},
            answer.id: {"format": "text", "value": "answer"},
        },
        "reviews": {
            review1.id: {
                "algorithm": "random",
                "card_id": card.id,
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "1",
            },
            review2.id: {
                "algorithm": "random",
                "card_id": card.id,
                "datetime": datetime.datetime(2021, 1, 1, 12, 00, 00, 000000),
                "result": "0",
            },
        },
        "tags": {tag2.id: {"name": "test-tag-2"}, tag1.id: {"name": "test-tag-1"}},
        "cardtags": {cardtag_id: {"card_id": card.id, "tag_id": tag2.id}},
        "decktags": {decktag_id: {"deck_id": deck.id, "tag_id": tag1.id}},
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
        serialize_uuids(
            {
                "decks": {
                    deck.id: {
                        "name": "Test",
                        "description": "A long description for deck",
                        "algorithm": "random",
                        "state": {},
                        "parameters": {},
                    }
                }
            }
        ),
        sort_keys=True,
    )
