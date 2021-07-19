from flashcards_core.schedulers.random import RandomScheduler


SCHEDULERS = [
    RandomScheduler,
]


def get_available_schedulers():
    return [scheduler.algorithm_name for scheduler in SCHEDULERS]


def get_scheduler(algorithm_name: str):
    """
    Scans all the available engines to look for the one
    that matches the given name.

    NOTE: The number of engines should be limited, so this
    procedure should be quite fast
    """
    for scheduler in SCHEDULERS:
        if scheduler.algorithm_name == algorithm_name:
            return scheduler
    raise ValueError(
        f"No engine found for algorithm '{algorithm_name}' "
        f"(available engines: {[e.algorith_name for e in SCHEDULERS]})"
    )
