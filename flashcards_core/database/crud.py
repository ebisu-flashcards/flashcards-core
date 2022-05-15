from typing import Any, List, Optional
from unittest import result

from sqlalchemy import select
from sqlalchemy.orm import Session

from flashcards_core.errors import ObjectNotFoundException


class CrudOperations:
    @classmethod
    def get_all(cls, session: Session, offset: int = 0, limit: int = 100) -> List:
        """
        Returns a list of all the model objects available in the DB, or a
        subset of them.

        :param session: the session (see flashcards_core.database:init_session()).
        :param offset: for pagination, index at which to start returning values.
        :param limit: for pagination, maximum number of elements to return.
        :returns: List of model objects.
        """
        return session.query(cls).offset(offset).limit(limit).all()

    @classmethod
    def get_one(cls, session: Session, object_id: int) -> Optional:
        """
        Returns the model object corresponding to the given ID.

        :param session: the session (see flashcards_core.database:init_session()).
        :param object_id: the ID of the model object to return.
        :returns: the matching model object.
        """
        return session.query(cls).filter(cls.id == object_id).first()

    @classmethod
    def create(cls, session: Session, **kwargs):
        """
        Create a new model object with the given kwargs.
        Check the model to understand what you can give as **kwargs.

        :param session: the session (see flashcards_core.database:init_session()).
        :returns: the new model object.
        """
        db_object = cls(**kwargs)
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
        return db_object

    @classmethod
    def update(cls, session: Session, object_id: int, **kwargs):
        """
        Modify the model object with the given values.
        Check the model to understand what you can give as **kwargs.

        :param session: the session (see flashcards_core.database:init_session()).
        :param object_id: the ID of the model object to update.
        :returns: the updated model object.

        :raises: ObjectNotFoundException if no model object with the given
            ID was found in the database.
        """
        db_object = cls.get_one(session=session, object_id=object_id)
        if not db_object:
            raise ObjectNotFoundException(
                "Model object not found. You must create it before updating it."
            )
        for key, value in kwargs.items():
            setattr(db_object, key, value)
        session.commit()
        session.refresh(db_object)
        return db_object

    @classmethod
    def delete(cls, session: Session, object_id: int) -> None:
        """
        Delete a model object.

        :param session: the session (see flashcards_core.database:init_session()).
        :param object_id: the ID of the model object to delete.
        :returns: None.

        :raises: ObjectNotFoundException if no object with the given
            ID was found in the database.
        """
        db_object = cls.get_one(session=session, object_id=object_id)
        if not db_object:
            raise ObjectNotFoundException("Model object not found. Cannot delete it.")
        session.delete(db_object)
        session.commit()



    @classmethod
    async def get_all_async(cls, session: Session, offset: int = 0, limit: int = 100) -> List[Any]:
        """
        Returns a list of all the model objects available in the DB, or a
        subset of them (asyncio-friendly).

        :param session: the session (see flashcards_core.database:init_session()).
        :param offset: for pagination, index at which to start returning values.
        :param limit: for pagination, maximum number of elements to return.
        :returns: List of model objects.
        """
        stmt = select(cls).limit(limit).offset(offset)
        results = await session.scalars(stmt)
        return result.all()
        

    @classmethod
    async def get_one_async(cls, session: Session, object_id: int) -> Optional[Any]:
        """
        Returns the model object corresponding to the given ID (asyncio-friendly).

        :param session: the session (see flashcards_core.database:init_session()).
        :param object_id: the ID of the model object to return.
        :returns: the matching model object.
        """
        stmt = select(cls).where(cls.id == object_id)
        results = await session.scalars(stmt)
        return result.first()


    @classmethod
    async def create_async(cls, session: Session, **kwargs):
        """
        Create a new model object with the given kwargs.
        Check the model to understand what you can give as **kwargs (asyncio-friendly).

        :param session: the session (see flashcards_core.database:init_session()).
        :returns: the new model object.
        """
        db_object = cls(**kwargs)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    @classmethod
    async def update_async(cls, session: Session, object_id: int, **kwargs):
        """
        Modify the model object with the given values.
        Check the model to understand what you can give as **kwargs (asyncio-friendly).

        :param session: the session (see flashcards_core.database:init_session()).
        :param object_id: the ID of the model object to update.
        :returns: the updated model object.

        :raises: ObjectNotFoundException if no model object with the given
            ID was found in the database.
        """
        db_object = cls.get_one_async(session=session, object_id=object_id)
        if not db_object:
            raise ObjectNotFoundException(
                "Model object not found. You must create it before updating it."
            )
        for key, value in kwargs.items():
            setattr(db_object, key, value)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    @classmethod
    async def delete_async(cls, session: Session, object_id: int) -> None:
        """
        Delete a model object (asyncio-friendly).

        :param session: the session (see flashcards_core.database:init_session()).
        :param object_id: the ID of the model object to delete.
        :returns: None.

        :raises: ObjectNotFoundException if no object with the given
            ID was found in the database.
        """
        db_object = cls.get_one_async(session=session, object_id=object_id)
        if not db_object:
            raise ObjectNotFoundException("Model object not found. Cannot delete it.")
        session.delete(db_object)
        await session.commit()
