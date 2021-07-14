from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.decks.model import Deck



def get_decks(db: Session, offset: int = 0, limit: int = 100) -> List[Deck]:
    """
    Returns a list of all the Deck model objects available in the DB, or a 
    subset of them.

    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).
    :param skip: for pagination, index at which to start returning values.
    :param limit: for pagination, maximum number of elements to return.

    :returns: List of Deck model objects.
    """
    return db.query(Deck).offset(offset).limit(limit).all()


def get_deck(db: Session, deck_id: int) -> Optional[Deck]:
    """
    Returns the Deck model object corresponding to the given ID.

    :param deck_id: the ID of the Deck model object to return.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the matching Deck model object.
    """
    return db.query(Deck).filter(Deck.id == deck_id).first()


def create_deck(db: Session, deck_name: str, deck_desc: str) -> Deck:
    """
    Create a new Deck model object with the given deck_name.

    :param deck_name: the name of the Deck model object to create.
    :param deck_desc: a short description of the deck
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new Deck model object.

    :raises: ValueError if a deck with the same name already exists.
    """
    if db.query(Deck).filter(Deck.name == deck_name).first():
        raise ValueError(f"An deck named '{deck_name}' already exists. Cannot create duplicate decks.")
    db_deck = Deck(name=deck_name, description=deck_desc)
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck


def update_deck(db: Session, deck_id: int, deck_name: str, deck_desc: str) -> Deck:
    """
    Update a Deck model object with the given values.

    :param deck_id: the ID of the Deck model object to update.
    :param deck_name: the new name of the Deck model object.
    :param deck_desc: the new description of the deck
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the updated Deck model object.

    :raises: ValueError if no deck with the given ID was found in the database.
    """
    db_deck = get_deck(deck_id=deck_id)
    if not db_deck:
        raise ValueError(f"Deck '{deck_id}' not found. Create it before updating it.")
    db_deck.update(name=deck_name, desc=deck_desc)
    db.commit()
    db.refresh(db_deck)
    return db_deck


def delete_deck(db: Session, deck_id: int) -> None:
    """
    Delete a Deck model object.

    :param deck_id: the ID of the Deck model object to delete.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no deck with the given ID was found in the database.
    """
    db_deck = get_deck(deck_id=deck_id)
    if not db_deck:
        raise ValueError(f"Deck '{deck_id}' not found. Cannot delete non-existing deck.")
    db.delete(db_deck)
    db.commit()
