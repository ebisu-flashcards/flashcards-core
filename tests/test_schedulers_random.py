import pytest
import random
import datetime
from freezegun import freeze_time

from flashcards_core.errors import NoCardsToStudyException
from flashcards_core.database import Deck, Card, Fact
from flashcards_core.schedulers.random import (
    RandomScheduler,
    NEVER_REPEAT,
    LAST_REVIEWED_CARD,
    UNSEEN_FIRST,
)


@pytest.fixture
def deck(session):
    return Deck.create(
        session=session, name="test-deck", description="test", algorithm="random"
    )


@pytest.fixture
def fact(session):
    return Fact.create(session=session, value="test-fact", format="text")


def test_random_create_scheduler(session, deck):
    scheduler = RandomScheduler(session=session, deck=deck)
    assert scheduler


def test_random_process_test_result_card_not_in_deck(session, deck, fact):
    wrong_deck = Deck.create(
        session=session, name="wrong-deck", description="test", algorithm="random"
    )
    card = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    scheduler = RandomScheduler(session=session, deck=wrong_deck)
    assert len(card.reviews) == 0
    with pytest.raises(ValueError):
        scheduler.process_test_result(card=card, result=True)
    assert len(card.reviews) == 0


@freeze_time("2021-01-01 12:00:00")
def test_random_process_test_result_card_in_deck(session, deck, fact):
    card = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    scheduler = RandomScheduler(session=session, deck=deck)
    assert len(card.reviews) == 0
    scheduler.process_test_result(card=card, result=True)
    assert len(card.reviews) == 1
    assert card.reviews[0].datetime == datetime.datetime.now()
    assert deck.state[LAST_REVIEWED_CARD] == card.id.hex


def test_random_next_card_no_cards(session, deck):
    scheduler = RandomScheduler(session=session, deck=deck)
    with pytest.raises(NoCardsToStudyException):
        scheduler.next_card()


def test_random_next_card_one_card_no_params(session, deck, fact):
    card = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    scheduler = RandomScheduler(session=session, deck=deck)
    for i in range(3):
        assert card == scheduler.next_card()


def test_random_next_card_one_card_never_repeat(session, deck, fact):
    deck.parameters = {NEVER_REPEAT: True}
    card = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    scheduler = RandomScheduler(session=session, deck=deck)
    for i in range(3):
        assert card == scheduler.next_card()


def test_random_next_card_two_cards_no_params(session, deck, fact):
    card1 = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    card2 = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    random.seed(12345)
    scheduler = RandomScheduler(session=session, deck=deck)

    assert card2 == scheduler.next_card()
    scheduler.process_test_result(card=card2, result=True)

    assert card1 == scheduler.next_card()
    scheduler.process_test_result(card=card1, result=True)

    assert card2 == scheduler.next_card()
    scheduler.process_test_result(card=card2, result=True)

    assert card2 == scheduler.next_card()  # Repetition is possible
    scheduler.process_test_result(card=card2, result=True)

    assert card1 == scheduler.next_card()
    scheduler.process_test_result(card=card1, result=True)

    assert card2 == scheduler.next_card()


def test_random_next_card_two_cards_never_repeat(session, deck, fact):
    deck.parameters = {NEVER_REPEAT: True}
    card1 = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    card2 = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    random.seed(12345)
    scheduler = RandomScheduler(session=session, deck=deck)
    for i in range(10):
        if i % 2 == 1:
            assert card1 == scheduler.next_card()
            scheduler.process_test_result(card=card1, result=True)
        else:
            assert card2 == scheduler.next_card()
            scheduler.process_test_result(card=card2, result=True)


def test_random_next_card_two_cards_unseen_first(session, deck, fact):
    random.seed(12345)
    scheduler = RandomScheduler(session=session, deck=deck)
    for i in range(10):
        card = Card.create(
            session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
        )
        scheduler.process_test_result(card=card, result=True)
    unseen_card = Card.create(
        session=session, deck_id=deck.id, question_id=fact.id, answer_id=fact.id
    )
    deck.parameters[UNSEEN_FIRST] = True
    Deck.update(session=session, object_id=deck.id, parameters=deck.parameters)
    assert unseen_card == scheduler.next_card()
