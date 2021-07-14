from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.many_to_many.model import FaceFact, DeckTag, CardTag, FaceTag, FactTag


#
#  FaceFact
#

def assign_fact_to_face(db: Session, fact_id: int, face_id: int) -> FaceFact:
    """
    Assign the given Fact to a given Face.

    :param fact_id: the name of the Fact to assign to the Face.
    :param face_id: the name of the Face to assign the Fact to.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new FaceFact model object.
    """
    db_facefact = FaceFact(fact_id=fact_id, face_id=face_id)
    db.add(db_facefact)
    db.commit()
    db.refresh(db_facefact)
    return db_facefact


def remove_fact_from_face(db: Session, facefact_id: int) -> None:
    """
    Remove the given Fact from the given Face.

    :param facefact_id: the ID of the connection between a fact and a face.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no FaceFact object with the given ID was found in the database.
    """
    db_facefact = db.query(FaceFact).filter(FaceFact.id == facefact_id).first()
    if not db_facefact:
        raise ValueError(f"No FaceFact with ID '{facefact_id}' found. Cannot delete non-existing connection.")
    db.delete(db_facefact)
    db.commit()

#
#  DeckTag
#

def assign_tag_to_deck(db: Session, tag_id: int, deck_id: int) -> DeckTag:
    """
    Assign the given Tag to a given Deck.

    :param tag_id: the name of the Tag to assign to the Deck.
    :param deck_id: the name of the Deck to assign the Tag to.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new DeckTag model object.
    """
    db_decktag = DeckTag(tag_id=tag_id, deck_id=deck_id)
    db.add(db_decktag)
    db.commit()
    db.refresh(db_decktag)
    return db_decktag


def remove_tag_from_deck(db: Session, decktag_id: int) -> None:
    """
    Remove the given Tag from the given Deck.

    :param decktag_id: the ID of the connection between a tag and a deck.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no DeckTag object with the given ID was found in the database.
    """
    db_decktag = db.query(DeckTag).filter(DeckTag.id == decktag_id).first()
    if not db_decktag:
        raise ValueError(f"No DeckTag with ID '{decktag_id}' found. Cannot delete non-existing connection.")
    db.delete(db_decktag)
    db.commit()

#
#  CardTag
#

def assign_tag_to_card(db: Session, tag_id: int, card_id: int) -> CardTag:
    """
    Assign the given Tag to a given Card.

    :param tag_id: the name of the Tag to assign to the Card.
    :param card_id: the name of the Card to assign the Tag to.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new CardTag model object.
    """
    db_cardtag = CardTag(tag_id=tag_id, card_id=card_id)
    db.add(db_cardtag)
    db.commit()
    db.refresh(db_cardtag)
    return db_cardtag


def remove_tag_from_card(db: Session, cardtag_id: int) -> None:
    """
    Remove the given Tag from the given Card.

    :param cardtag_id: the ID of the connection between a tag and a card.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no CardTag object with the given ID was found in the database.
    """
    db_cardtag = db.query(CardTag).filter(CardTag.id == cardtag_id).first()
    if not db_cardtag:
        raise ValueError(f"No CardTag with ID '{cardtag_id}' found. Cannot delete non-existing connection.")
    db.delete(db_cardtag)
    db.commit()

#
#  FaceTag
#

def assign_tag_to_face(db: Session, tag_id: int, face_id: int) -> FaceTag:
    """
    Assign the given Tag to a given Face.

    :param tag_id: the name of the Tag to assign to the Face.
    :param face_id: the name of the Face to assign the Tag to.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new FaceTag model object.
    """
    db_facetag = FaceTag(tag_id=tag_id, face_id=face_id)
    db.add(db_facetag)
    db.commit()
    db.refresh(db_facetag)
    return db_facetag


def remove_tag_from_face(db: Session, facetag_id: int) -> None:
    """
    Remove the given Tag from the given Face.

    :param facetag_id: the ID of the connection between a tag and a face.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no FaceTag object with the given ID was found in the database.
    """
    db_facetag = db.query(FaceTag).filter(FaceTag.id == facetag_id).first()
    if not db_facetag:
        raise ValueError(f"No FaceTag with ID '{facetag_id}' found. Cannot delete non-existing connection.")
    db.delete(db_facetag)
    db.commit()
#
#  FaceTag
#

def assign_tag_to_fact(db: Session, tag_id: int, fact_id: int) -> FactTag:
    """
    Assign the given Tag to a given Fact.

    :param tag_id: the name of the Tag to assign to the Fact.
    :param fact_id: the name of the Fact to assign the Tag to.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new FactTag model object.
    """
    db_facttag = FactTag(tag_id=tag_id, fact_id=fact_id)
    db.add(db_facttag)
    db.commit()
    db.refresh(db_facttag)
    return db_facttag


def remove_tag_from_fact(db: Session, facttag_id: int) -> None:
    """
    Remove the given Tag from the given Fact.

    :param facttag_id: the ID of the connection between a tag and a fact.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no FactTag object with the given ID was found in the database.
    """
    db_facttag = db.query(FactTag).filter(FactTag.id == facttag_id).first()
    if not db_facttag:
        raise ValueError(f"No FactTag with ID '{facttag_id}' found. Cannot delete non-existing connection.")
    db.delete(db_facttag)
    db.commit()
