
class BaseAlgorithmEngine:

    #: The algorithm ID associated with this engine
    algorithm_name = None

    def __init__(self):
        pass

    def next_card_to_review(self):
        raise NotImplementedError("This is the base class, use an implementation.")

    def process_test_result(self, card_id=card_id, test_results=test_results):
        """
        Creates a Review for the card, storing the test result.

        :param card_id: the card that was reviewed
        :param test_results: the results of the test
        :return: None
        """
        raise NotImplementedError("This is the base class, use an implementation.")
