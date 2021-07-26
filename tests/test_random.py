from flashcards_core.database import Deck, Card
from flashcards_core.schedulers import RandomScheduler


def test_random(session):
    """
    Test that the Random algorithm works as espected.

    FIXME this is a stub!
    """
    deck = Deck.create(session=session, name="TestDeck", description="Test Deck")
    deck.set_state(session=session, state={"unseen_first": True, "never_repeat": True})
    card = Card.create(session=session, deck_id=deck.id)
    card = Card.create(session=session, deck_id=deck.id)
    card = Card.create(session=session, deck_id=deck.id)

    engine = RandomScheduler(session=session, deck=deck)

    for i in range(7):
        card = engine.next_card()
        print(card)
        engine.process_test_result(card, True)
