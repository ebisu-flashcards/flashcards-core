from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.algorithm_params.model import AlgorithmParam



def get_algorithm_params(db: Session, offset: int = 0, limit: int = 100) -> List[AlgorithmParam]:
    """
    Returns a list of all the AlgorithmParam model objects available in the DB, or a 
    subset of them.

    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).
    :param skip: for pagination, index at which to start returning values.
    :param limit: for pagination, maximum number of elements to return.

    :returns: List of AlgorithmParam model objects.
    """
    return db.query(AlgorithmParam).offset(offset).limit(limit).all()


def get_algorithm_param(db: Session, algorithm_param_id: int) -> Optional[AlgorithmParam]:
    """
    Returns the AlgorithmParam model object corresponding to the given ID.

    :param algorithm_param_id: the ID of the AlgorithmParam model object to return.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the matching AlgorithmParam model object.
    """
    return db.query(AlgorithmParam).filter(AlgorithmParam.id == algorithm_param_id).first()


def create_algorithm_param(db: Session, algorithm_id: int, deck_id: int, values: str) -> AlgorithmParam:
    """
    Create a new AlgorithmParam model object with the given algorithm_param_name.

    :param algorithm_id: the name of the algorithm this parameters refer to.
    :param deck_id: the name of the deck that uses this parameters.
    :param values: the actual parameters, stored as JSON.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new AlgorithmParam model object.

    :raises: ValueError if a algorithm_param with the same name already exists.
    """
    db_algorithm_param = AlgorithmParam(algorithm_id=algorithm_id, deck_id=deck_id, values=values)
    db.add(db_algorithm_param)
    db.commit()
    db.refresh(db_algorithm_param)
    return db_algorithm_param


def update_algorithm_param(db: Session, algorithm_param_id: int, algorithm_id: int, 
        deck_id: int, values: str) -> AlgorithmParam:
    """
    Update a AlgorithmParam model object with the given values.

    :param algorithm_param_id: the ID of the AlgorithmParam model object to update.
    :param algorithm_id: the name of the algorithm this parameters refer to.
    :param deck_id: the name of the deck that uses this parameters.
    :param values: the actual parameters, stored as JSON.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the updated AlgorithmParam model object.

    :raises: ValueError if no algorithm_param with the given ID was found in the database.
    """
    db_algorithm_param = get_algorithm_param(algorithm_param_id=algorithm_param_id)
    if not db_algorithm_param:
        raise ValueError(f"AlgorithmParam '{algorithm_param_id}' not found. Create it before updating it.")
    db_algorithm_param.update(name=algorithm_param_name)
    db.commit()
    db.refresh(db_algorithm_param)
    return db_algorithm_param


def delete_algorithm_param(db: Session, algorithm_param_id: int) -> None:
    """
    Delete a AlgorithmParam model object.

    :param algorithm_param_id: the ID of the AlgorithmParam model object to delete.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no algorithm_param with the given ID was found in the database.
    """
    db_algorithm_param = get_algorithm_param(algorithm_param_id=algorithm_param_id)
    if not db_algorithm_param:
        raise ValueError(f"AlgorithmParam '{algorithm_param_id}' not found. Cannot delete non-existing algorithm parameters.")
    db.delete(db_algorithm_param)
    db.commit()
