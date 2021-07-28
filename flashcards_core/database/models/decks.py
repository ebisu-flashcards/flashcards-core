from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Table, JSON
from sqlalchemy.orm import relationship, Session
from sqlalchemy_json import mutable_json_type

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Tags
#

DeckTag = Table(
    "decktags",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("deck_id", Integer, ForeignKey("decks.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Deck(Base, CrudOperations):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    algorithm = Column(String, nullable=False)
    parameters = Column(
        mutable_json_type(dbtype=JSON, nested=True), nullable=False, default={}
    )
    state = Column(
        mutable_json_type(dbtype=JSON, nested=True), nullable=False, default={}
    )

    cards = relationship("Card", cascade="all,delete", back_populates="deck")
    tags = relationship("Tag", secondary="decktags")

    def __repr__(self):
        return f"<Deck '{self.name}' (ID: {self.id})>"

    @classmethod
    def get_by_name(cls, session: Session, name: str) -> Optional:
        """
        Returns the deck corresponding to the given name.

        :param session: the session (see flashcards_core.database:init_db()).
        :param name: the name of the model object to return.
        :returns: the matching model object.
        """
        return session.query(Deck).filter(Deck.name == name).first()

    def unseen_cards_list(self) -> List:
        """
        Return a list of all the cards belonging to this deck that have no Reviews,
        which means they have never been seen/reviewed.
        """
        # FIXME Redo as a proper SQL query!!!
        return [card for card in self.cards if len(card.reviews) == 0]

    def unseen_cards_number(self) -> int:
        """
        Return the number of cards belonging to this deck that have no Reviews,
        which means they have never been seen/reviewed.
        """
        # FIXME Redo as a proper SQL query!!!
        return len([card for card in self.cards if len(card.reviews) == 0])

    def assign_tag(self, session: Session, tag_id: int) -> None:
        """
        Assign the given Tag to this Deck and refreshes the Deck object.

        :param tag_id: the name of the Tag to assign to the Deck.
        :param session: the session (see flashcards_core.database:init_db()).
        """
        insert = DeckTag.insert().values(deck_id=self.id, tag_id=tag_id)
        session.execute(insert)
        session.refresh(self)

    def remove_tag(self, session: Session, tag_id: int) -> None:
        """
        Remove the given Tag from this Deck.

        :param tag_id: the ID of the tag to remove from this deck
        :param session: the session (see flashcards_core.database:init_db()).
        :returns: None.
        :raises: ValueError if no tag object with the given ID was assigned to this deck.
        """
        delete = DeckTag.delete().where(DeckTag.c.tag_id == tag_id)
        session.execute(delete)
        session.refresh(self)
