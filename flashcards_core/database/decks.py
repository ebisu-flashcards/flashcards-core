from typing import Any, Dict, List

import json

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table
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
    name = Column(String, index=True)
    description = Column(String)
    state = Column(
        String, default="{}"
    )  # JSON for all the mixed stuff: params, state, etc...

    algorithm_id = Column(Integer, ForeignKey("algorithms.id"))
    algorithm = relationship("Algorithm", foreign_keys="Deck.algorithm_id")

    cards = relationship("Card", back_populates="deck")
    tags = relationship("Tag", secondary="DeckTag", backref="Deck")

    def __repr__(self):
        return f"<Deck '{self.name}' (ID: {self.id})>"

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

    def unseen_cards_list(self) -> List["Card"]:
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
