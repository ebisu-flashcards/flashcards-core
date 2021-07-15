import logging
from flashcards_core.algorithm_engines.base import BaseAlgorithmEngine


class RandomEngine(BaseAlgorithmEngine):

    algorithm_name = "Random"

    def __init__(self):
        super(self).__init__()


    # def process_test_result(self, card_id=card_id, test_results=test_results) -> None:
    #     """
    #     Creates a Review for the card, storing the test result.

    #     In a Random deck there is no further processing to do,
    #     except storing a pointer to the last card in case the
    #     deck is configured to never show the same card twice in
    #     a row. In addition, storing Reviews is useful to keep track
    #     of Unseen cards, if so requested, and for later statistics.

    #     A Random deck will probably store boolean results, but in 
    #     practice this is not mandatory and the frontend can choose
    #     to send any value here. Therefore, the results field is not
    #     typed.

    #     :param card_id: the card that was reviewed
    #     :param test_results: the results of the test
    #     :return: None
    #     """       
    #     try:
    #         logging.debug(f"Creating Review for Card ID {card_id} "
    #                       f"with result {test_results} "
    #                       f"at time {datetime.utcnow())}"

    #         user = User.objects.get(id=user_id)
    #         review = Review(
    #             user=user, 
    #             test_results=results, 
    #             review_time=datetime.utcnow()
    #         )
    #         self.deck.reviewing_card.update(push__reviews=review)
    #         self.deck.reviewing_card.save()
        
    #     except mongoengine.errors.DoesNotExist as e:
    #         # Logs the issue, but it's not critical - just return
    #         logging.error("MongoEngine threw an exception!", e)
    #         logging.warning("Exception can be ignored, going ahead")
    #         pass


    # def next_card_to_review(self) -> 'Card':
    #     """ 
    #     Picks a random card. 
    #     Avoids repeating the same card twice if so required and possible (i.e there is more than 1 card). 
    #     Gives priority to unseen cards if so required.
    #     """
    #     logging.debug("Finding next card to review")

    #     cards = Card.objects(deck=self.deck.id).all()
    #     if len(cards) == 0:
    #         raise errors.NoCardsToReviewError("No cards present in this deck")
        
    #     # Update last reviewed card field
    #     reviewing_card = self.deck.reviewing_card
    #     self.deck.update(last_reviewed_card=reviewing_card)
        
    #     # Select random unseen card, if unseen cards have priority
    #     new_cards = self.new_cards()
    #     if self.deck.prioritize_unseen and len(new_cards) > 0:
    #         reviewing_card = random.choice(new_cards)

    #     # Avoid asking twice the same card in a row if required and possible
    #     elif self.deck.consecutive_never_identical and len(cards) > 1:
    #         while reviewing_card == self.deck.last_reviewed_card:
    #             reviewing_card = random.choice(cards)

    #     # Last check to make sure we return a card in any case
    #     if not reviewing_card:
    #         reviewing_card = random.choice(cards)

    #     # Save and return
    #     self.deck.update(reviewing_card=reviewing_card)
    #     self.deck.save()
    #     self.deck.reload()
    #     return self.deck.reviewing_card
