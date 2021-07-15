from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Tags
#

FactTag = Table(
    "FactTag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("fact_id", Integer, ForeignKey("facts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Fact(Base, CrudOperations):
    __tablename__ = "facts"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String)  # Can be text, a URL, a path, etc. Figure this out better.

    faces = relationship("Face", secondary="FaceFact", back_populates="facts")
    tags = relationship("Tag", secondary="FactTag", backref="Fact")

    def __repr__(self):
        return (
            f"<Fact '{self.value if len(self.value) < 20 else self.value[:20] + '...'}'"
            f" (ID: {self.id})>"
        )

    def assign_tag(self, db: Session, tag_id: int) -> FactTag:
        """
        Assign the given Tag to this Fact.

        :param tag_id: the name of the Tag to assign to the Fact.
        :param fact_id: the name of the Fact to assign the Tag to.
        :param db: the session (see flashcards_core.database:SessionLocal()).

        :returns: the new FactTag model object.
        """
        db_facttag = FactTag(tag_id=tag_id, fact_id=self.id)
        db.add(db_facttag)
        db.commit()
        db.refresh(db_facttag)
        return db_facttag

    def remove_tag(self, db: Session, facttag_id: int) -> None:
        """
        Remove the given Tag from this Fact.

        :param facttag_id: the ID of the connection between a tag and a fact.
        :param db: the session (see flashcards_core.database:SessionLocal()).

        :returns: None.

        :raises: ValueError if no FactTag object with the given ID was found in the database.
        """
        db_facttag = db.query(FactTag).filter(FactTag.id == facttag_id).first()
        if not db_facttag:
            raise ValueError(
                f"No FactTag with ID '{facttag_id}' found. Cannot delete non-existing"
                " connection."
            )
        db.delete(db_facttag)
        db.commit()
