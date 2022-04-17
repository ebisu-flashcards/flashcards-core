from typing import Any
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from flashcards_core.database import Deck, Card


class BaseScheduler(ABC):
    def __init__(self, session: Session, deck: Deck):

        #: The session to use to interact with the database
        self.session = session

        #: The deck we're studying
        self.deck = deck

    @abstractmethod
    def next_card(self) -> Card:
        """
        :return: the next card to review
        """
        raise NotImplementedError("This is the base class, use an implementation.")

    @abstractmethod
    def process_test_result(self, card: Card, result: Any):
        """
        Creates a Review for the card, storing the test result.

        Different implementations might use a different type for the results,
        therefore this parameter is not typed.

        :param card: the card that was reviewed
        :param result: the results of the test
        :return: None
        """
        raise NotImplementedError("This is the base class, use an implementation.")
