from typing import Any

import json
import random
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from flashcards_core.database import Deck, Card, Review
from flashcards_core.algorithm_engines.base import BaseAlgorithmEngine


UNSEEN_FIRST = "unseen_first"
NEVER_REPEAT = "never_repeat"
LAST_REVIEWED_CARD = "last_reviewed_card"


class RandomEngine(BaseAlgorithmEngine):

    algorithm_name = "Random"

    def __init__(self, db: Session, deck: Deck):
        super().__init__(db=db, deck=deck)

    def next_card(self) -> Card:
        """
        Returns the next card to review.

        In a Random deck, this is any random card.
        If the deck is configured to give priority to unseen
        cards (`unseen_first: true`) then the new card is chosen
        among the new ones, if any.
        If the deck is configured to never show the same card twice
        in a row (`never_repeat: true`), and the deck has more than
        one card, then this method makes sure this constraints is
        respected.

        :param deck: the deck to pick the next card from
        :return: the next Card to study
        """
        logging.debug(f"Picking the next card to review from deck {self.deck} ")
        logging.debug(
            f"Deck state: {self.deck.get_state()}. Unseen cards:"
            f" {self.deck.unseen_cards_number()}"
        )
        logging.debug(f"This deck has {len(self.deck.cards)} cards.")

        if len(self.deck.cards) == 0:
            raise ValueError("Cannot study from an empty deck.")

        if len(self.deck.cards) == 1:
            return self.deck.cards[0]

        # Give priority to unseen cards if configured to do so
        deck_state = self.deck.get_state()
        if deck_state.get(UNSEEN_FIRST) and self.deck.unseen_cards_number() > 0:
            logging.debug(
                f"Picking from the {self.deck.unseen_cards_number()} unseen cards"
            )
            return random.choice(self.deck.unseen_cards_list())

        next_card = random.choice(self.deck.cards)
        logging.debug(f"Picked card ID {next_card.id}")

        # Avoid repeating cards if configured to do so
        if deck_state.get(NEVER_REPEAT):

            last_card_id = deck_state.get(LAST_REVIEWED_CARD)
            while last_card_id == next_card.id:
                logging.debug(
                    f"It's the same card as last time ({last_card_id}), retrying"
                )

                next_card = random.choice(self.deck.cards)
                logging.debug(f"Picked card ID {next_card.id}")

        return next_card

    def process_test_result(self, card: Card, result: Any) -> None:
        """
        Creates a Review for the card, storing the test result.

        In a Random deck there is no further processing to do,
        except storing a pointer to the last card in case the
        deck is configured to never show the same card twice in
        a row. In addition, storing Reviews is useful to keep track
        of Unseen cards, if so requested, and for later statistics.

        A Random deck will probably store boolean results, but in
        practice this is not mandatory and the frontend can choose
        to send any value here. Therefore, the results field is not
        typed.

        :param card: the card that was reviewed
        :param test_results: the results of the test
        :return: None

        :raise: ValueError if the card does not belong to the deck
        """
        if card.deck != self.deck:
            raise ValueError(f"This card belongs to another deck ({card.deck}).")

        logging.debug(
            f"Creating Review for Card '{card}'' "
            f"with result '{result}' "
            f"at time (approx.) {datetime.utcnow()}"
        )

        # Create the review
        review = Review.create(db=self.db, card_id=card.id, result=result)

        # Update the deck state
        deck_state = card.deck.get_state()
        deck_state[LAST_REVIEWED_CARD] = card.id
        card.deck.set_state(db=self.db, state=deck_state)
