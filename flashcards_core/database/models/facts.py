from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship, Session

from flashcards_core.guid import GUID
from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Tags
#

FactTag = Table(
    "facttags",
    Base.metadata,
    Column("id", GUID(), primary_key=True, default=uuid4),
    Column("fact_id", GUID(), ForeignKey("facts.id")),
    Column("tag_id", GUID(), ForeignKey("tags.id")),
)


class Fact(Base, CrudOperations):
    __tablename__ = "facts"

    #: Primary key
    id = Column(GUID(), primary_key=True, index=True, default=uuid4)

    #: The content of this fact. Can be plaintext, html,
    #: markdown, a URL, a path to a file... Use the content
    #: of `Fact.format` to understando how to decode this field.
    value = Column(String, nullable=False)

    #: How to interpret the content of `Fact.value`.
    #: It's up to the frontend application to decide how to
    #: represent the card, but this field should give a good
    #: hint. For example, it can have values like 'plaintext',
    #: 'markdown', 'image', 'url', etc.
    format = Column(String, nullable=False)  # How to read the content of 'value'

    #: All the tags assigned to this fact
    tags = relationship("Tag", secondary="facttags")

    def __repr__(self):
        return (
            f"<Fact '{self.value if len(self.value) < 20 else self.value[:20] + '...'}'"
            f" (ID: {self.id})>"
        )

    def assign_tag(self, session: Session, tag_id: int) -> FactTag:
        """
        Assign the given Tag to this Fact.

        :param tag_id: the name of the Tag to assign to the Fact.
        :param session: the session (see flashcards_core.database:init_db()).
        """
        insert = FactTag.insert().values(fact_id=self.id, tag_id=tag_id)
        result = session.execute(insert)
        session.refresh(self)
        return result

    def remove_tag(self, session: Session, tag_id: int) -> None:
        """
        Remove the given Tag from this Fact.

        :param facttag_id: the ID of the connection between a tag and a fact.
        :param session: the session (see flashcards_core.database:init_db()).

        :returns: None.
        """
        delete = FactTag.delete().where(FactTag.c.tag_id == tag_id)
        session.execute(delete)
        session.refresh(self)
