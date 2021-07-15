from flashcards_core.algorithm_engines.random import RandomEngine

ENGINES = [
    RandomEngine,
]

def get_algorithm_engine(self, algorithm_name: str):
    """
    Scans all the available engines to look for the one
    that matches the given name.

    NOTE: The number of engines should be limited, so this
    procedure should be quite fast
    """
    for engine in ENGINES:
        if engine.algorithm_name == algorithm_name:
            return engine
    raise ValueError(f"No engine found for algorithm '{algorithm_name}' "
                     f"(available engines: {[e.algorith_name for e in ENGINES]})")