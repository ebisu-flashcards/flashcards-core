import datetime
from freezegun import freeze_time

from flashcards_core.database import Card, Review, Deck, Fact


@freeze_time("2021-01-01 12:00:00")
def test_review_create_review_no_card(session):
    review = Review.create(session=session, result="result", algorithm="a")
    assert review
    assert review.datetime == datetime.datetime.now()


@freeze_time("2021-01-01 12:00:00")
def test_review_create(session):
    deck = Deck.create(
        session=session, name="test", description="test", algorithm="test"
    )
    question = Fact.create(session=session, value="question", format="plaintext")
    answer = Fact.create(session=session, value="answer", format="plaintext")
    card = Card.create(
        session=session, deck_id=deck.id, question_id=question.id, answer_id=answer.id
    )
    review = Review.create(
        session=session, result="review", algorithm="a", card_id=card.id
    )
    assert review
    assert review.datetime == datetime.datetime.now()


@freeze_time("2021-01-01 12:00:00")
def test_review_repr(session):
    deck = Deck.create(
        session=session, name="test", description="test", algorithm="test"
    )
    question = Fact.create(session=session, value="question", format="plaintext")
    answer = Fact.create(session=session, value="answer", format="plaintext")
    card = Card.create(
        session=session, deck_id=deck.id, question_id=question.id, answer_id=answer.id
    )
    review = Review.create(
        session=session, result="review", algorithm="a", card_id=card.id
    )
    assert (
        f"<Review of card #{card.id}: 'review' at 2021-01-01 12:00:00 (ID: {review.id})>"
        == f"{review}"
    )
