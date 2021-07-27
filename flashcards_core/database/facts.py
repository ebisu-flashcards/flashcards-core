from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Tags
#

FactTag = Table(
    "facttags",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("fact_id", Integer, ForeignKey("facts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Fact(Base, CrudOperations):
    __tablename__ = "facts"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)  # Can be text, URL, path, etc.
    format = Column(String, nullable=False)  # How to read the content of 'value'
    # FIXME add some sort of metadata here too?
    #   Question/answers have them on the card already

    tags = relationship("Tag", secondary="facttags", backref="Fact")

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
        session.execute(insert)
        session.refresh(self)

    def remove_tag(self, session: Session, tag_id: int) -> None:
        """
        Remove the given Tag from this Fact.

        :param facttag_id: the ID of the connection between a tag and a fact.
        :param session: the session (see flashcards_core.database:init_db()).

        :returns: None.

        :raises: ValueError if no FactTag object with the given ID was found in the database.
        """
        delete = FactTag.delete().where(FactTag.c.tag_id == tag_id)
        session.execute(delete)
        session.refresh(self)
