from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_core.database.database import Base


class Fact(Base):
    __tablename__ = "facts"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String)  # Can be text, a URL, a path, etc. Figure this out better.
    
    faces = relationship('Face', secondary='FaceFact', back_populates="facts")
    tags = relationship('Tag', secondary='FactTag', backref='Fact')


    def __repr__(self):
        return f"<Fact '{self.value if len(self.value) < 20 else self.value[:20] + '...'}' (ID: {self.id})>"