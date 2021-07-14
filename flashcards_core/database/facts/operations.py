from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.facts.model import Fact



def get_facts(db: Session, offset: int = 0, limit: int = 100) -> List[Fact]:
    """
    Returns a list of all the Fact model objects available in the DB, or a 
    subset of them.

    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).
    :param skip: for pagination, index at which to start returning values.
    :param limit: for pagination, maximum number of elements to return.

    :returns: List of Fact model objects.
    """
    return db.query(Fact).offset(offset).limit(limit).all()


def get_fact(db: Session, fact_id: int) -> Optional[Fact]:
    """
    Returns the Fact model object corresponding to the given ID.

    :param fact_id: the ID of the Fact model object to return.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the matching Fact model object.
    """
    return db.query(Fact).filter(Fact.id == fact_id).first()


def create_fact(db: Session, fact_value: str) -> Fact:
    """
    Create a new Fact model object with the given fact_name.

    :param fact_value: the text representation of this fact. 
        Can be text, a url, a path, etc...
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new Fact model object.

    :raises: ValueError if a fact with the same value already exists.
    """
    if db.query(Fact).filter(Fact.value == fact_value).first():
        raise ValueError(f"An fact with value '{fact_value}' already exists. Cannot create duplicate facts.")
    db_fact = Fact(value=fact_value)
    db.add(db_fact)
    db.commit()
    db.refresh(db_fact)
    return db_fact


def update_fact(db: Session, fact_id: int, fact_value: str) -> Fact:
    """
    Update a Fact model object with the given values.

    :param fact_id: the ID of the Fact model object to update.
    :param fact_value: the text representation of this fact. 
        Can be text, a url, a path, etc...
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the updated Fact model object.

    :raises: ValueError if no fact with the given ID was found in the database.
    """
    db_fact = get_fact(fact_id=fact_id)
    if not db_fact:
        raise ValueError(f"Fact '{fact_id}' not found. Create it before updating it.")
    db_fact.update(value=fact_value)
    db.commit()
    db.refresh(db_fact)
    return db_fact


def delete_fact(db: Session, fact_id: int) -> None:
    """
    Delete a Fact model object.

    :param fact_id: the ID of the Fact model object to delete.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no fact with the given ID was found in the database.
    """
    db_fact = get_fact(fact_id=fact_id)
    if not db_fact:
        raise ValueError(f"Fact '{fact_id}' not found. Cannot delete non-existing fact.")
    db.delete(db_fact)
    db.commit()
