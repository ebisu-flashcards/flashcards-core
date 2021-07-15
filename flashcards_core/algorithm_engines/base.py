from typing import Any

from sqlalchemy.orm import Session

from flashcards_core.database import Deck, Card, Review


class BaseAlgorithmEngine:

    #: The algorithm ID associated with this engine
    algorithm_name = None

    def __init__(self, db: Session, deck: Deck):
        
        #: The session to use to interact with the database
        self.db = db

        #: The deck we're studying
        self.deck = deck

    def next_card(self) -> Card:
        """
        Creates a Review for the card, storing the test result.

        :param card: the card that was reviewed
        :param test_results: the results of the test
        :return: None

        :raise: ValueError if the card does not belong to the deck
        """
        raise NotImplementedError("This is the base class, use an implementation.")

    def process_test_result(self, card: Card, test_results: Any):
        """
        Creates a Review for the card, storing the test result.

        Different implementations might use a different type for the results,
        therefore this parameter is not typed.

        :param card_id: the card that was reviewed
        :param test_results: the results of the test
        :return: None
        """
        raise NotImplementedError("This is the base class, use an implementation.")
