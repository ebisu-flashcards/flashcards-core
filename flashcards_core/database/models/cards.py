from uuid import uuid4, UUID
from sqlalchemy import Column, ForeignKey, Table, String
from sqlalchemy.orm import relationship, Session, backref

from flashcards_core.guid import GUID
from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations, AsyncCrudOperations


#: Associative table for Cards and Tags
CardTag = Table(
    "cardtags",
    Base.metadata,
    Column("card_id", GUID(), ForeignKey("cards.id"), primary_key=True),
    Column("tag_id", GUID(), ForeignKey("tags.id"), primary_key=True),
)

#: Associative table for Cards and question context Facts
CardQuestionContext = Table(
    "card_question_contextes",
    Base.metadata,
    Column("card_id", GUID(), ForeignKey("cards.id"), primary_key=True),
    Column("fact_id", GUID(), ForeignKey("facts.id"), primary_key=True),
)

#: Associative table for Cards and answer context Facts
CardAnswerContext = Table(
    "card_answer_contextes",
    Base.metadata,
    Column("card_id", GUID(), ForeignKey("cards.id"), primary_key=True),
    Column("fact_id", GUID(), ForeignKey("facts.id"), primary_key=True),
)

#: Associative table for Cards relationships
RelatedCard = Table(
    "related_cards",
    Base.metadata,
    Column("original_card_id", GUID(), ForeignKey("cards.id"), primary_key=True),
    Column("related_card_id", GUID(), ForeignKey("cards.id"), primary_key=True),
    Column("relationship", String),
)


class _Card(Base):
    __tablename__ = "cards"

    #: Primary key
    id = Column(GUID(), primary_key=True, index=True, default=uuid4)

    #: ID to the deck this card belongs to.
    #: Note that this is a one-to-many repationship because it
    #: should be easy to copy cards.
    #: Cards hold no actual data: it's just an associative table
    deck_id = Column(GUID(), ForeignKey("decks.id"), nullable=False)

    #: The deck this card belongs to.
    #: Note that this is a one-to-many repationship because it
    #: should be easy to copy cards.
    #: Cards hold no actual data: it's just an associative table
    deck = relationship("Deck", foreign_keys="Card.deck_id")

    #: ID of the fact containing the question of this card.
    question_id = Column(GUID(), ForeignKey("facts.id"), nullable=False)

    #: The fact containing the question of this card.
    question = relationship("Fact", foreign_keys="Card.question_id")

    #: All the facts containing some context for the question.
    #: You can add as many facts as you wish for cards questions.
    question_context_facts = relationship("Fact", secondary="card_question_contextes")

    #: ID of the fact containing the answer of this card.
    answer_id = Column(GUID(), ForeignKey("facts.id"), nullable=False)

    #: The fact containing the answer of this card.
    answer = relationship("Fact", foreign_keys="Card.answer_id")

    #: All the facts containing some context for the answer.
    #: You can add as many facts as you wish for cards answers.
    answer_context_facts = relationship("Fact", secondary="card_answer_contextes")

    #: All the cards that are somehow related to the current one
    #: Relationships are named (to help discoverability), see RelatedCards
    related_cards = relationship(
        "Card",
        secondary=RelatedCard,
        primaryjoin=(RelatedCard.c.original_card_id == id),
        secondaryjoin=(RelatedCard.c.related_card_id == id),
        backref=backref("original_card_id", lazy="select"),
        lazy="select",
    )

    #: All the reviews done on this card.
    reviews = relationship("Review", cascade="all,delete", back_populates="card")

    #: All the tags assigned to this card
    tags = relationship("Tag", secondary="cardtags")

    def __repr__(self):
        return f"<Card (ID: {self.id}, deck ID: {self.deck_id})>"

    def assign_tag(self, session: Session, tag_id: UUID) -> None:
        """
        Assign the given Tag to this Card.

        :param tag_id: the name of the Tag to assign to the Card.
        :param session: the session (see flashcards_core.database:init_db())
        """
        insert = CardTag.insert().values(card_id=self.id, tag_id=tag_id)
        session.execute(insert)
        session.commit()
        session.refresh(self)

    def remove_tag(self, session: Session, tag_id: UUID) -> None:
        """
        Remove the given Tag from this Card.

        :param tag_id: the ID of the connection between a tag and a card.
        :param session: the session (see flashcards_core.database:init_db()).
        """
        delete = CardTag.delete().where(CardTag.c.tag_id == tag_id)
        session.execute(delete)
        session.commit()
        session.refresh(self)

    def assign_question_context(self, session: Session, fact_id: UUID) -> None:
        """
        Assign the given Fact as context to the Question to this Card.

        :param fact_id: the name of the Fact to assign as context to the question
            of this card.
        :param session: the session (see flashcards_core.database:init_db()).
        """
        insert = CardQuestionContext.insert().values(card_id=self.id, fact_id=fact_id)
        session.execute(insert)
        session.commit()
        session.refresh(self)

    def remove_question_context(self, session: Session, fact_id: UUID) -> None:
        """
        Remove the given Fact as a context for the Question from this Card.

        :param fact_id: the ID of the fact to remove from the answer's context
        :param session: the session (see flashcards_core.database:init_db()).
        """
        delete = CardQuestionContext.delete().where(
            CardQuestionContext.c.fact_id == fact_id
        )
        session.execute(delete)
        session.commit()
        session.refresh(self)

    def assign_answer_context(self, session: Session, fact_id: UUID) -> None:
        """
        Assign the given Fact as context to the Answer to this Card.

        :param fact_id: the name of the Fact to assign as context to the answer
            of this card.
        :param session: the session (see flashcards_core.database:init_db()).
        """
        insert = CardAnswerContext.insert().values(card_id=self.id, fact_id=fact_id)
        session.execute(insert)
        session.commit()
        session.refresh(self)

    def remove_answer_context(self, session: Session, fact_id: UUID) -> None:
        """
        Remove the given Fact as a context for the Answer from this Card.

        :param fact_id: the ID of the fact to remove from the answer's context
        :param session: the session (see flashcards_core.database:init_db()).
        """
        delete = CardAnswerContext.delete().where(
            CardAnswerContext.c.fact_id == fact_id
        )
        session.execute(delete)
        session.commit()
        session.refresh(self)


class Card(_Card, CrudOperations):
    pass

class ACard(_Card, AsyncCrudOperations):
    pass