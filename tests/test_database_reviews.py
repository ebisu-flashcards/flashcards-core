from flashcards_core.database import Card, Review


def test_review_create_review_no_card(session):
    assert Review.create(session=session, result="result", algorithm="a")


def test_review_create(session):
    card = Card.create(session=session)
    assert Review.create(
        session=session, result="review", algorithm="a", card_id=card.id
    )


def test_review_repr(session):
    card = Card.create(session=session)
    review = Review.create(
        session=session, result="review", algorithm="a", card_id=card.id
    )
    assert "<Review of card ID: 1: review (ID: 1)>" == f"{review}"
