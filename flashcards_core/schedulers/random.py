from typing import Any

import random
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from flashcards_core.database import Deck, Card, Review
from flashcards_core.schedulers.base import BaseScheduler

#
# Parameter keys for RandomScheduler
#

#: Pick the next card from the unseen ones, if any
UNSEEN_FIRST = "unseen_first"

#: Never pick the same card twice in a row,
#:   if there is more than one card in the deck
NEVER_REPEAT = "never_repeat"

#
# State keys for RandomScheduler
#

#: ID of the last card reviewed
LAST_REVIEWED_CARD = "last_reviewed_card"


class RandomScheduler(BaseScheduler):
    def __init__(self, session: Session, deck: Deck, _seed: int = None):
        super().__init__(session=session, deck=deck)
        if _seed:
            random.seed(_seed)

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
        logging.debug(f"Picking the next card to review from deck {self.deck}")
        logging.debug(f"This deck has {len(self.deck.cards)} cards.")
        logging.debug(f"Deck params: {self.deck.parameters}")
        logging.debug(f"Deck state: {self.deck.state}")
        logging.debug(f"Unseen cards: {self.deck.unseen_cards_number()}")

        if len(self.deck.cards) == 0:
            raise ValueError("Cannot study on an empty deck.")

        if len(self.deck.cards) == 1:
            return self.deck.cards[0]

        # Give priority to unseen cards if configured to do so
        if (
            self.deck.parameters.get(UNSEEN_FIRST)
            and self.deck.unseen_cards_number() > 0
        ):
            logging.debug("Picking from the unseen cards")
            return random.choice(self.deck.unseen_cards_list())

        # Pick the next card
        next_card = random.choice(self.deck.cards)
        logging.debug(f"Picked card #{next_card.id}")

        # Avoid repeating cards if configured to do so
        if self.deck.parameters.get(NEVER_REPEAT):
            last_card_id = self.deck.state.get(LAST_REVIEWED_CARD)
            while last_card_id == next_card.id:
                logging.debug(f"It's the same card (#{last_card_id}), retrying")
                next_card = random.choice(self.deck.cards)

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
        :param result: the results of the test
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
        Review.create(
            session=self.session,
            card_id=card.id,
            result=result,
            algorithm=self.deck.algorithm,
        )

        # Update the deck state
        self.deck.state[LAST_REVIEWED_CARD] = card.id
        self.deck = Deck.update(
            session=self.session, object_id=card.deck.id, state=self.deck.state
        )
        logging.debug(f"New deck state: {self.deck.state}")
