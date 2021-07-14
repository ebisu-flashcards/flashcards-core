from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.tags.model import Tag as TagModel



def get_tags(db: Session, offset: int = 0, limit: int = 100) -> List[TagModel]:
    """
    Returns a list of all the Tag model objects available in the DB, or a 
    subset of them.

    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).
    :param skip: for pagination, index at which to start returning values.
    :param limit: for pagination, maximum number of elements to return.

    :returns: List of Tag model objects.
    """
    return db.query(TagModel).offset(offset).limit(limit).all()


def get_tag(db: Session, tag_id: int) -> Optional[TagModel]:
    """
    Returns the Tag model object corresponding to the given ID.

    :param tag_id: the ID of the Tag model object to return.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the matching Tag model object.
    """
    return db.query(TagModel).filter(TagModel.id == tag_id).first()


def create_tag(db: Session, tag_name: str) -> TagModel:
    """
    Create a new Tag model object with the given tag_name.

    :param tag_name: the name of the Tag model object to create.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new Tag model object.

    :raises: ValueError if a tag with the same name already exists.
    """
    if db.query(TagModel).filter(TagModel.name == tag_name).first():
        raise ValueError(f"A tag named '{tag_name}' already exists. Cannot create duplicate tags.")
    db_tag = TagModel(name=tag_name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(db: Session, tag_id: int, tag_name: str) -> TagModel:
    """
    Update a Tag model object with the given tag_name.

    :param tag_id: the ID of the Tag model object to update.
    :param tag_name: the new name of the Tag model object.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the updated Tag model object.

    :raises: ValueError if no tag with the given ID was found in the database.
    """
    db_tag = get_tag(tag_id=tag_id)
    if not db_tag:
        raise ValueError(f"Tag '{tag_id}' not found. Create it before updating it.")
    db_tag.update(name=tag_name)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int) -> None:
    """
    Delete a Tag model object.

    :param tag_id: the ID of the Tag model object to delete.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no tag with the given ID was found in the database.
    """
    db_tag = get_tag(tag_id=tag_id)
    if not db_tag:
        raise ValueError(f"Tag '{tag_id}' not found. Cannot delete non-existing tag.")
    db.delete(db_tag)
    db.commit()
