from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.algorithms.model import Algorithm



def get_algorithms(db: Session, offset: int = 0, limit: int = 100) -> List[Algorithm]:
    """
    Returns a list of all the Algorithm model objects available in the DB, or a 
    subset of them.

    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).
    :param skip: for pagination, index at which to start returning values.
    :param limit: for pagination, maximum number of elements to return.

    :returns: List of Algorithm model objects.
    """
    return db.query(Algorithm).offset(offset).limit(limit).all()


def get_algorithm(db: Session, algorithm_id: int) -> Optional[Algorithm]:
    """
    Returns the Algorithm model object corresponding to the given ID.

    :param algorithm_id: the ID of the Algorithm model object to return.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the matching Algorithm model object.
    """
    return db.query(Algorithm).filter(Algorithm.id == algorithm_id).first()


def create_algorithm(db: Session, algorithm_name: str) -> Algorithm:
    """
    Create a new Algorithm model object with the given values.

    :param algorithm_name: the name of the Algorithm model object to create.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new Algorithm model object.

    :raises: ValueError if a algorithm with the same name already exists.
    """
    if db.query(Algorithm).filter(Algorithm.name == algorithm_name).first():
        raise ValueError(f"An algorithm named '{algorithm_name}' already exists. Cannot create duplicate algorithms.")
    db_algorithm = Algorithm(name=algorithm_name)
    db.add(db_algorithm)
    db.commit()
    db.refresh(db_algorithm)
    return db_algorithm


def update_algorithm(db: Session, algorithm_id: int, algorithm_name: str) -> Algorithm:
    """
    Update a Algorithm model object with the given algorithm_name.

    :param algorithm_id: the ID of the Algorithm model object to update.
    :param algorithm_name: the new name of the Algorithm model object.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the updated Algorithm model object.

    :raises: ValueError if no algorithm with the given ID was found in the database.
    """
    db_algorithm = get_algorithm(algorithm_id=algorithm_id)
    if not db_algorithm:
        raise ValueError(f"Algorithm '{algorithm_id}' not found. Create it before updating it.")
    db_algorithm.update(name=algorithm_name)
    db.commit()
    db.refresh(db_algorithm)
    return db_algorithm


def delete_algorithm(db: Session, algorithm_id: int) -> None:
    """
    Delete a Algorithm model object.

    :param algorithm_id: the ID of the Algorithm model object to delete.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no algorithm with the given ID was found in the database.
    """
    db_algorithm = get_algorithm(algorithm_id=algorithm_id)
    if not db_algorithm:
        raise ValueError(f"Algorithm '{algorithm_id}' not found. Cannot delete non-existing algorithm.")
    db.delete(db_algorithm)
    db.commit()
