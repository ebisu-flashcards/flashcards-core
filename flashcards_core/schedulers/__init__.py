from flashcards_core.schedulers.random import RandomScheduler


SCHEDULERS = {
    "Random": RandomScheduler,
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
        raise ValueError(
            f"No schedulers found for algorithm '{algorithm_name}' "
            f"(available schedulers: {[s.algorith_name for s in SCHEDULERS]})"
        )
    return scheduler


def get_scheduler_for_deck(db, deck):
    """
    Returns a ready-to-use scheduler for the algorithm assigned to this deck.

    :param db: the session (see flashcards_core.database:SessionLocal()).
    :param deck: the deck this scheduler is generated for
    :returns: a subclass of BaseScheduler
    """
    scheduler_class = get_scheduler_class(deck.algorithm)
    return scheduler_class(db=db, deck=deck)
