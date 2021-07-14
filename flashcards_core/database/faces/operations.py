from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.faces.model import Face



def get_faces(db: Session, offset: int = 0, 
        limit: int = 100) -> List[Face]:
    """
    Returns a list of all the Face model objects available in the DB, or a 
    subset of them.

    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).
    :param skip: for pagination, index at which to start returning values.
    :param limit: for pagination, maximum number of elements to return.

    :returns: List of Face model objects.
    """
    return db.query(Face).offset(offset).limit(limit).all()


def get_face(db: Session, face_id: int) -> Optional[Face]:
    """
    Returns the Face model object corresponding to the given ID.

    :param face_id: the ID of the Face model object to return.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the matching Face model object.
    """
    return db.query(Face).filter(Face.id == face_id).first()


def create_face(db: Session, card_id: int, reveal_order: float) -> Face:
    """
    Create a new Face model object with the given face_name.

    :param card_id: the card this Face object it tied to
    :param reveal_order: the order in which this face will 
        be revealed (if relevant).
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new Face model object.
    """
    db_face = Face(card_id=card_id, reveal_order=reveal_order)
    db.add(db_face)
    db.commit()
    db.refresh(db_face)
    return db_face


def update_face(db: Session, face_id: int, card_id: int, reveal_order: float) -> Face:
    """
    Update a Face model object with the given values.

    :param face_id: the ID of the Face model object to update.
    :param card_id: the card this Face object it tied to
    :param reveal_order: the order in which this face will 
        be revealed (if relevant).
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the updated Face model object.

    :raises: ValueError if no face with the given ID was found in the database.
    """
    db_face = get_face(face_id=face_id)
    if not db_face:
        raise ValueError(f"Face '{face_id}' not found. Create it before updating it.")
    db_face.update(card_id=card_id, reveal_order=reveal_order)
    db.commit()
    db.refresh(db_face)
    return db_face


def delete_face(db: Session, face_id: int) -> None:
    """
    Delete a Face model object.

    :param face_id: the ID of the Face model object to delete.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no face with the given ID was found in the database.
    """
    db_face = get_face(face_id=face_id)
    if not db_face:
        raise ValueError(f"Face '{face_id}' not found. Cannot delete non-existing face.")
    db.delete(db_face)
    db.commit()
