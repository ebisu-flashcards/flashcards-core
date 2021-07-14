from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table

from flashcards_core.database.database import Base


FaceFact = Table('FaceFact',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('face_id', Integer, ForeignKey('faces.id')),
    Column('fact_id', Integer, ForeignKey('facts.id')),
)

DeckTag = Table('DeckTag',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('deck_id', Integer, ForeignKey('decks.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

CardTag = Table('CardTag',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)

FaceTag = Table('FaceTag',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('face_id', Integer, ForeignKey('faces.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)

FactTag = Table('FactTag',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('fact_id', Integer, ForeignKey('facts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)