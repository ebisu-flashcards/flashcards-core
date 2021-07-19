from typing import Any, Dict, List, Optional

import json

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Tags
#

DeckTag = Table(
    "DeckTag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("deck_id", Integer, ForeignKey("decks.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Deck(Base, CrudOperations):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    algorithm = Column(String)
    parameters = Column(String, default="{}")  # FIXME JSON field
    state = Column(String, default="{}")  # FIXME JSON field

    cards = relationship("Card", cascade="all,delete", back_populates="deck")
    tags = relationship("Tag", secondary="DeckTag", backref="Deck")

    def __repr__(self):
        return f"<Deck '{self.name}' (ID: {self.id})>"

    @classmethod
    def get_by_name(cls, db: Session, name: str) -> Optional:
        """
        Returns the deck corresponding to the given name.

        :param db: the session (see flashcards_core.database:SessionLocal()).
        :param name: the name of the model object to return.
        :returns: the matching model object.
        """
        return db.query(Deck).filter(Deck.name == name).first()

    def get_parameters(self) -> Dict[str, Any]:
        """
        Returns the parameters of the deck as a dictionary, obtained by loading
        the field `parameters` as JSON.

        Please do not read/write this field directly, but use the getter/setter.
        """
        return json.loads(self.parameters)

    def set_parameters(self, db: Session, parameters: Dict[str, Any]):
        """
        Sets the parameters of the deck from the dictionary, by dumping the value
        in the `parameters` field as JSON

        Please do not read/write this field directly, but use the getter/setter.
        """
        self.parameters = json.dumps(parameters)
        db.commit()
        db.refresh(self)

    def get_state(self) -> Dict[str, Any]:
        """
        Returns the state of the deck as a dictionary, obtained by loading
        the field `state` as JSON.

        Please do not read/write this field directly, but use the getter/setter.
        """
        return json.loads(self.state)

    def set_state(self, db: Session, state: Dict[str, Any]):
        """
        Sets the state of the deck from the dictionary, by dumping the value
        in the `state` field as JSON

        Please do not read/write this field directly, but use the getter/setter.
        """
        self.state = json.dumps(state)
        db.commit()
        db.refresh(self)

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
            raise ValueError(
                f"No DeckTag with ID '{decktag_id}' found. Cannot delete non-existing"
                " connection."
            )
        db.delete(db_decktag)
        db.commit()
