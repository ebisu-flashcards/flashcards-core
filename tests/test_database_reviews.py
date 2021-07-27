import datetime
from freezegun import freeze_time

from flashcards_core.database import Card, Review


@freeze_time("2021-01-01 12:00:00")
def test_review_create_review_no_card(session):
    review = Review.create(session=session, result="result", algorithm="a")
    assert review
    assert review.datetime == datetime.datetime.now()


@freeze_time("2021-01-01 12:00:00")
def test_review_create(session):
    card = Card.create(session=session, deck_id=1, question_id=1, answer_id=1)
    review = Review.create(
        session=session, result="review", algorithm="a", card_id=card.id
    )
    assert review
    assert review.datetime == datetime.datetime.now()


@freeze_time("2021-01-01 12:00:00")
def test_review_repr(session):
    card = Card.create(session=session, deck_id=1, question_id=1, answer_id=1)
    review = Review.create(
        session=session, result="review", algorithm="a", card_id=card.id
    )
    assert "<Review of card #1: 'review' at 2021-01-01 12:00:00 (ID: 1)>" == f"{review}"
