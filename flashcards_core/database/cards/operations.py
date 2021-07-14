from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.cards.model import Card



def get_cards(db: Session, offset: int = 0, limit: int = 100) -> List[Card]:
    """
    Returns a list of all the Card model objects available in the DB, or a 
    subset of them.

    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).
    :param skip: for pagination, index at which to start returning values.
    :param limit: for pagination, maximum number of elements to return.

    :returns: List of Card model objects.
    """
    return db.query(Card).offset(offset).limit(limit).all()


def get_card(db: Session, card_id: int) -> Optional[Card]:
    """
    Returns the Card model object corresponding to the given ID.

    :param card_id: the ID of the Card model object to return.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the matching Card model object.
    """
    return db.query(Card).filter(Card.id == card_id).first()


def create_card(db: Session, deck_id: int) -> Card:
    """
    Create a new Card model object with the given card_name.

    :param deck_id: the ID of the deck this card belongs to.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new Card model object.
    """
    db_card = Card(deck_id=deck_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def delete_card(db: Session, card_id: int) -> None:
    """
    Delete a Card model object.

    :param card_id: the ID of the Card model object to delete.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no card with the given ID was found in the database.
    """
    db_card = get_card(card_id=card_id)
    if not db_card:
        raise ValueError(f"Card '{card_id}' not found. Cannot delete non-existing card.")
    db.delete(db_card)
    db.commit()
