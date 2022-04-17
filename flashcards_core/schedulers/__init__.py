from flashcards_core.errors import ObjectNotFoundException
from flashcards_core.schedulers.base import BaseScheduler
from flashcards_core.schedulers.random import RandomScheduler


# FIXME we could make algorithms pluggable instead of hardcoding them all... right?
SCHEDULERS = {
    "random": RandomScheduler,
}


def get_available_schedulers():
    """
    Returns a list of the known algorithm (scheduler) names.
    """
    return SCHEDULERS.keys()


def get_scheduler_class(algorithm_name: str):
    """
    Returns the scheduler class corresponding to the given name.
    """
    scheduler = SCHEDULERS.get(algorithm_name, None)
    if not scheduler:
        raise ObjectNotFoundException(
            f"No schedulers found for algorithm '{algorithm_name}' "
            f"(available schedulers: {list(SCHEDULERS.keys())})"
        )
    return scheduler


def get_scheduler_for_deck(session, deck):
    """
    Returns a ready-to-use scheduler for the algorithm assigned to this deck.

    :param session: the session (see flashcards_core.database:init_db()).
    :param deck: the deck this scheduler is generated for
    :returns: a subclass of BaseScheduler
    """
    scheduler_class = get_scheduler_class(deck.algorithm)
    return scheduler_class(session=session, deck=deck)
