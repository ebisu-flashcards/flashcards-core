from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship

from flashcards_core.database.database import Base


class Face(Base):
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