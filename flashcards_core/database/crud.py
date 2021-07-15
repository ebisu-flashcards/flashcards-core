from typing import List, Optional

from sqlalchemy.orm import Session


class CrudOperations:
    @classmethod
    def get_all(cls, db: Session, offset: int = 0, limit: int = 100) -> List:
        """
        Returns a list of all the model objects available in the DB, or a
        subset of them.

        :param db: the session (see flashcards_core.database:SessionLocal()).
        :param skip: for pagination, index at which to start returning values.
        :param limit: for pagination, maximum number of elements to return.
        :returns: List of model objects.
        """
        return db.query(cls).offset(offset).limit(limit).all()

    @classmethod
    def get_one(cls, db: Session, object_id: int) -> Optional:
        """
        Returns the model object corresponding to the given ID.

        :param db: the session (see flashcards_core.database:SessionLocal()).
        :param algorithm_param_id: the ID of the model object to return.
        :returns: the matching model object.
        """
        return db.query(cls).filter(cls.id == object_id).first()

    @classmethod
    def create(cls, db: Session, **kwargs):
        """
        Create a new model object with the given kwargs.
        Check the model to understand what you can give as **kwargs.

        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: the new model object.
        """
        db_object = cls(**kwargs)
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    @classmethod
    def update(cls, db: Session, object_id: int, **kwargs):
        """
        Modify the model object with the given values.
        Check the model to understand what you can give as **kwargs.

        :param db: the session (see flashcards_core.database:SessionLocal()).
        :param object_id: the ID of the model object to update.
        :returns: the updated model object.

        :raises: ValueError if no model object with the given ID was found in the database.
        """
        db_object = cls.get_one(db=db, object_id=object_id)
        if not db_object:
            raise ValueError(
                "Model object not found. You must create it before updating it."
            )
        for key, value in kwargs.items():
            setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)
        return db_object

    @classmethod
    def delete(cls, db: Session, object_id: int) -> None:
        """
        Delete a model object.

        :param db: the session (see flashcards_core.database:SessionLocal()).
        :param object_id: the ID of the model object to delete.
        :returns: None.

        :raises: ValueError if no algorithm_param with the given ID was found in the database.
        """
        db_object = cls.get_one(db=db, object_id=object_id)
        if not db_object:
            raise ValueError("Model object not found. Cannot delete it.")
        db.delete(db_object)
        db.commit()
