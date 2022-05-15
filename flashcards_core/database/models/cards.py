from typing import List

from uuid import uuid4, UUID
from sqlalchemy import Column, ForeignKey, Table, String
from sqlalchemy.orm import relationship, Session, backref

from flashcards_core.guid import GUID
from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


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


class Card(Base, CrudOperations):
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
    deck = relationship("Deck", foreign_keys="Card.deck_id", lazy='selectin')

    #: ID of the fact containing the question of this card.
    question_id = Column(GUID(), ForeignKey("facts.id"), nullable=False)

    #: The fact containing the question of this card.
    question = relationship("Fact", foreign_keys="Card.question_id", lazy='selectin')

    #: All the facts containing some context for the question.
    #: You can add as many facts as you wish for cards questions.
    question_context_facts = relationship("Fact", secondary="card_question_contextes", lazy='selectin')

    #: ID of the fact containing the answer of this card.
    answer_id = Column(GUID(), ForeignKey("facts.id"), nullable=False)

    #: The fact containing the answer of this card.
    answer = relationship("Fact", foreign_keys="Card.answer_id", lazy='selectin')

    #: All the facts containing some context for the answer.
    #: You can add as many facts as you wish for cards answers.
    answer_context_facts = relationship("Fact", secondary="card_answer_contextes", lazy='selectin')

    #: All the cards that are somehow related to the current one
    #: Relationships are named (to help discoverability), see RelatedCards
    related_cards = relationship(
        "Card",
        secondary=RelatedCard,
        primaryjoin=(RelatedCard.c.original_card_id == id),
        secondaryjoin=(RelatedCard.c.related_card_id == id),
        backref=backref("original_card_id"), 
        lazy='selectin')

    #: All the reviews done on this card.
    reviews = relationship("Review", cascade="all,delete", back_populates="card", lazy='selectin')

    #: All the tags assigned to this card
    tags = relationship("Tag", secondary="cardtags", lazy='selectin')

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

    async def assign_tag_async(self, session: Session, tag_id: UUID) -> None:
        """
        Assign the given Tag to this Card (asyncio friendly).

        :param tag_id: the name of the Tag to assign to the Card.
        :param session: the session (see flashcards_core.database:init_db())
        """
        insert = CardTag.insert().values(card_id=self.id, tag_id=tag_id)
        await session.execute(insert)
        await session.commit()
        await session.refresh(self)

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

    async def remove_tag_async(self, session: Session, tag_id: UUID) -> None:
        """
        Remove the given Tag from this Card (asyncio friendly).

        :param tag_id: the ID of the connection between a tag and a card.
        :param session: the session (see flashcards_core.database:init_db()).
        """
        delete = CardTag.delete().where(CardTag.c.tag_id == tag_id)
        await session.execute(delete)
        await session.commit()
        await session.refresh(self)

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

    async def assign_question_context_async(self, session: Session, fact_id: UUID) -> None:
        """
        Assign the given Fact as context to the Question to this Card (asyncio friendly).

        :param fact_id: the name of the Fact to assign as context to the question
            of this card.
        :param session: the session (see flashcards_core.database:init_db()).
        """
        insert = CardQuestionContext.insert().values(card_id=self.id, fact_id=fact_id)
        await session.execute(insert)
        await session.commit()
        await session.refresh(self)

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

    async def remove_question_context_async(self, session: Session, fact_id: UUID) -> None:
        """
        Remove the given Fact as a context for the Question from this Card (asyncio friendly).

        :param fact_id: the ID of the fact to remove from the answer's context
        :param session: the session (see flashcards_core.database:init_db()).
        """
        delete = CardQuestionContext.delete().where(
            CardQuestionContext.c.fact_id == fact_id
        )
        await session.execute(delete)
        await session.commit()
        await session.refresh(self)

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

    async def assign_answer_context_async(self, session: Session, fact_id: UUID) -> None:
        """
        Assign the given Fact as context to the Answer to this Card (asyncio friendly).

        :param fact_id: the name of the Fact to assign as context to the answer
            of this card.
        :param session: the session (see flashcards_core.database:init_db()).
        """
        insert = CardAnswerContext.insert().values(card_id=self.id, fact_id=fact_id)
        await session.execute(insert)
        await session.commit()
        await session.refresh(self)

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

    async def remove_answer_context_async(self, session: Session, fact_id: UUID) -> None:
        """
        Remove the given Fact as a context for the Answer from this Card (asyncio friendly).

        :param fact_id: the ID of the fact to remove from the answer's context
        :param session: the session (see flashcards_core.database:init_db()).
        """
        delete = CardAnswerContext.delete().where(
            CardAnswerContext.c.fact_id == fact_id
        )
        await session.execute(delete)
        await session.commit()
        await session.refresh(self)


    async def related_cards_async(self, session: Session) -> List["Card"]:
        """
        Returns all the related cards pairs in an asyncio friendly way.

        :returns: a list of Card with a "relationship" attribute, which
        contains the name of the relationship as it was stored in the RelatedCard
        associative table
        """
        stmt = RelatedCard.select().where(RelatedCard.c.original_card_id == self.id)
        pairs = await session.scalars(stmt)

        related_cards = []
        for pair in pairs:
            card = await Card.get_one_async(session=session, object_id=pair.related_card_id)
            card.relationship = pair.relationship
            related_cards.append(card)

        return related_cards

    def assign_related_card(self, session: Session, card_id: UUID, relationship: str) -> None:
        """
        Create a relationship between these two Cards.

        :param card_id: the name of the other Card.
        :param relationship: the type of relationship between these Cards
        :param session: the session (see flashcards_core.database:init_db()).
        """
        insert = RelatedCard.insert().values(original_card_id=self.id, related_card_id=card_id, relationship=relationship)
        session.execute(insert)
        session.commit()
        session.refresh(self)

    async def assign_related_card_async(self, session: Session, card_id: UUID, relationship: str) -> None:
        """
        Create a relationship between these two Cards (asyncio friendly).

        :param card_id: the name of the other Card.
        :param relationship: the type of relationship between these Cards
        :param session: the session (see flashcards_core.database:init_db()).
        """
        insert = RelatedCard.insert().values(original_card_id=self.id, related_card_id=card_id, relationship=relationship)
        await session.execute(insert)
        await session.commit()
        await session.refresh(self)

    def remove_related_card(self, session: Session, card_id: UUID) -> None:
        """
        Remove the relationship between these two Cards

        :param card_id: the ID of the relationship between these two Cards
        :param session: the session (see flashcards_core.database:init_db()).
        """
        delete = RelatedCard.delete().where(RelatedCard.c.related_card_id == card_id)
        session.execute(delete)
        session.commit()
        session.refresh(self)

    async def remove_related_card_async(self, session: Session, card_id: UUID) -> None:
        """
        Remove the relationship between these two Cards (asyncio friendly)

        :param card_id: the ID of the relationship between these two Cards
        :param session: the session (see flashcards_core.database:init_db()).
        """
        delete = RelatedCard.delete().where(RelatedCard.c.related_card_id == card_id)
        await session.execute(delete)
        await session.commit()
        await session.refresh(self)