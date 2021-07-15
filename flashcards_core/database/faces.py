from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Table
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Facts
#

FaceFact = Table('FaceFact',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('face_id', Integer, ForeignKey('faces.id')),
    Column('fact_id', Integer, ForeignKey('facts.id')),
)


#
# Many2Many with Tags
#

FaceTag = Table('FaceTag',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('face_id', Integer, ForeignKey('faces.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)


class Face(Base, CrudOperations):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True, index=True)

    reveal_order = Float(Integer)  # To always allow extra stages to go in between existing ones
    
    # Card is 12M because it should be easy to copy faces.
    # Faces hold no actual data: it's just an associative table
    card_id = Column(Integer, ForeignKey('cards.id'))
    card = relationship("Card", foreign_keys='Face.card_id')

    facts = relationship('Fact', secondary='FaceFact', back_populates="faces")
    tags = relationship('Tag', secondary='FaceTag', backref='Face')

    def __repr__(self):
        return f"<Face (ID: {self.id}, card ID: {self.card_id})>"

    
    def assign_fact(self, db: Session, fact_id: int) -> FaceFact:
        """
        Assign the given Fact to this Face.

        :param db: the session (see flashcards_core.database:SessionLocal()).
        :param fact_id: the name of the Fact to assign to the Face.
        :returns: the new FaceFact model object.
        """
        db_facefact = FaceFact(fact_id=fact_id, face_id=self.id)
        db.add(db_facefact)
        db.commit()
        db.refresh(db_facefact)
        return db_facefact


    def remove_fact(self, db: Session, facefact_id: int) -> None:
        """
        Remove the given Fact from this Face.

        :param db: the session (see flashcards_core.database:SessionLocal()).
        :param facefact_id: the ID of the connection between a fact and a face.
        :returns: None.

        :raises: ValueError if no FaceFact object with the given ID was found in the database.
        """
        db_facefact = db.query(FaceFact).filter(FaceFact.id == facefact_id).first()
        if not db_facefact:
            raise ValueError(f"No FaceFact with ID '{facefact_id}' found. Cannot delete non-existing connection.")
        db.delete(db_facefact)
        db.commit()


    def assign_tag(self, db: Session, tag_id: int) -> FaceTag:
        """
        Assign the given Tag to this Face.

        :param tag_id: the name of the Tag to assign to the Face.
        :param face_id: the name of the Face to assign the Tag to.
        :param db: the session (see flashcards_core.database:SessionLocal()).

        :returns: the new FaceTag model object.
        """
        db_facetag = FaceTag(tag_id=tag_id, face_id=self.id)
        db.add(db_facetag)
        db.commit()
        db.refresh(db_facetag)
        return db_facetag


    def remove_tag(self, db: Session, facetag_id: int) -> None:
        """
        Remove the given Tag from this Face.

        :param facetag_id: the ID of the connection between a tag and a face.
        :param db: the session (see flashcards_core.database:SessionLocal()).

        :returns: None.

        :raises: ValueError if no FaceTag object with the given ID was found in the database.
        """
        db_facetag = db.query(FaceTag).filter(FaceTag.id == facetag_id).first()
        if not db_facetag:
            raise ValueError(f"No FaceTag with ID '{facetag_id}' found. Cannot delete non-existing connection.")
        db.delete(db_facetag)
        db.commit()
