from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Tags
#

DeckTag = Table('DeckTag',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('deck_id', Integer, ForeignKey('decks.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Deck(Base, CrudOperations):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    # algorithm_id = Column(Integer, ForeignKey('algorithms.id'))
    # algorithm = relationship("Algorithm", foreign_keys='decks.algorithm_id')

    algorithm_params = relationship('AlgorithmParam', back_populates='deck')
    cards = relationship('Card', back_populates='deck')
    tags = relationship('Tag', secondary='DeckTag', backref='Deck')

    def __repr__(self):
        return f"<Deck '{self.name}' (ID: {self.id})>"

        
    def assign_tag(self, db: Session, tag_id: int, deck_id: int) -> DeckTag:
        """
        Assign the given Tag to this Deck.

        :param tag_id: the name of the Tag to assign to the Deck.
        :param deck_id: the name of the Deck to assign the Tag to.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: the new DeckTag model object.
        """
        db_decktag = DeckTag(tag_id=tag_id, deck_id=deck_id)
        db.add(db_decktag)
        db.commit()
        db.refresh(db_decktag)
        return db_decktag


    def remove_tag(self, db: Session, decktag_id: int) -> None:
        """
        Remove the given Tag from this Deck.

        :param decktag_id: the ID of the connection between a tag and a deck.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: None.
        :raises: ValueError if no DeckTag object with the given ID was found in the database.
        """
        db_decktag = db.query(DeckTag).filter(DeckTag.id == decktag_id).first()
        if not db_decktag:
            raise ValueError(f"No DeckTag with ID '{decktag_id}' found. Cannot delete non-existing connection.")
        db.delete(db_decktag)
        db.commit()
