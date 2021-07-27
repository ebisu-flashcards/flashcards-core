from typing import Any

from sqlalchemy.orm import Session

from flashcards_core.database.decks import Deck
from flashcards_core.database.cards import Card
from flashcards_core.schedulers import get_scheduler_for_deck


class Study:
    """
    Creates a study session by initializing an algorithm
    engine to process the cards once they're studied.

    This is more of a convenience class than an API, as all
    engines should be stateless.
    """

    def __init__(self, session: Session, deck: Deck):
        self.deck = deck
        self.scheduler = get_scheduler_for_deck(session=session, deck=deck)

    def next(self, studied_card: Card = None, result: Any = None) -> Card:
        """
        Saves the results of a test and returns the next card to be studied.

        :param studied_card: Card reviewed. Cano be None if the session just started.
        :param result: the result of the review. Type depends on the algorithm.
        :returns: the next Card to study
        """
        if studied_card:
            self.scheduler.process_test_result(card=studied_card, result=result)
        return self.scheduler.next_card()
