from typing import List, Optional

from sqlalchemy.orm import Session

from flashcards_core.database.database import SessionLocal
from flashcards_core.database.reviews.model import Review



def get_reviews(offset: int = 0, limit: int = 100) -> List[Review]:
    """
    Returns a list of all the Review model objects available in the DB, or a 
    subset of them.

    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).
    :param skip: for pagination, index at which to start returning values.
    :param limit: for pagination, maximum number of elements to return.

    :returns: List of Review model objects.
    """
    return db.query(Review).offset(offset).limit(limit).all()


def get_review(db: Session, review_id: int) -> Optional[Review]:
    """
    Returns the Review model object corresponding to the given ID.

    :param review_id: the ID of the Review model object to return.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the matching Review model object.
    """
    return db.query(Review).filter(Review.id == review_id).first()


def create_review(db: Session, result: str, card_id: int, algorithm_id: int) -> Review:
    """
    Create a new Review model object with the given values.

    :param result: the result of the review: success/failure for example.
    :param card_id: the card that was reviewed.
    :param algorithm_id: the algorithm used to study this card.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the new Review model object.

    :raises: ValueError if a review with the same name already exists.
    """
    db_review = Review(result=result, card_id=card_id, algorithm_id=algorithm_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(db: Session, review_id: int, result: str, card_id: int, 
        algorithm_id: int, ) -> Review:
    """
    Update a Review model object with the given review_name.

    :param review_id: the ID of the Review model object to update.
    :param result: the result of the review: success/failure for example.
    :param card_id: the card that was reviewed.
    :param algorithm_id: the algorithm used to study this card.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: the updated Review model object.

    :raises: ValueError if no review with the given ID was found in the database.
    """
    db_review = get_review(review_id=review_id)
    if not db_review:
        raise ValueError(f"Review '{review_id}' not found. Create it before updating it.")
    db_review.update(name=review_name)
    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review(db: Session, review_id: int) -> None:
    """
    Delete a Review model object.

    :param review_id: the ID of the Review model object to delete.
    :param db: the database session (if None, 
        flashcards_core.database.database:SessionLocal()).

    :returns: None.

    :raises: ValueError if no review with the given ID was found in the database.
    """
    db_review = get_review(review_id=review_id)
    if not db_review:
        raise ValueError(f"Review '{review_id}' not found. Cannot delete non-existing review.")
    db.delete(db_review)
    db.commit()
