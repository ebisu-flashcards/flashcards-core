from typing import Any, Mapping

from flashcards_core.algorithm_engines import get_algorithm_engine
from flashcards_core.database.decks import Deck


class SpacedRepetition:
    def __init__(self, deck: Deck):
        """
        Create a SpacedRepetition object for a given deck.
        The deck is used mainly to create the proper AlgorithmEngine.
        """
        self.engine = get_algorithm_engine(deck.algorithm_id)

    def next_card(self, deck_id: str):
        """
        Returns the next card in the deck to be studied.

        :param deck_id: Deck to take the card from
        :returns: a database Card object.
        """
        return self.engine.next_card_to_review()

    def save_test_results(self, card_id: str, test_results: Mapping[str, Any]) -> None:
        """
        Saves the results of a test.

        :param card_id: Card reviewed
        :param test_results: the content of the form of the user, as a dictionary.
            Passed to the algorihtm as a series of arg=value.
        :returns: Nothing.
        :raises Card.DoesNotExist if the card does not exist in this deck
        :raises Deck.DoesNotExist if the deck does not exist for this user
        """
        return self.engine.process_test_result(
            card_id=card_id, test_results=test_results
        )
