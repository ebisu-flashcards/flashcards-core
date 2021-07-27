import pytest
import random

from flashcards_core.database import Deck, Card, Fact
from flashcards_core.study import Study


@pytest.fixture
def deck(session):
    deck = Deck.create(session=session, name="a", description="a", algorithm="random")
    fact = Fact.create(session=session, value="b", format="b")
    Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    return deck


def test_study(session, deck):
    random.seed(12345)
    study = Study(session=session, deck=deck)
    card = study.next()
    assert card
    assert study.next(card, True)
