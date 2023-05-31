from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


# SQL Relationships:
class UserTable(Base):
    __tablename__ = 'UserTable'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    nationality = Column(String)


class GameTable(Base):
    __tablename__ = 'GameTable'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    price = Column(Integer)
    age_range = Column(Integer)


class PurchaseTable(Base):
    __tablename__ = 'PurchaseTable'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('GameTable.id'))
    user_id = Column(Integer, ForeignKey('UserTable.id'))
    price = Column(Integer)
    date = Column(Integer)
    game = relationship('GameTable', backref='purchases')
    user = relationship('UserTable', backref='purchases')


class ReviewTable(Base):
    __tablename__ = 'ReviewTable'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('GameTable.id'))
    message = Column(String)
    rating = Column(Integer)
    game = relationship('GameTable', backref='reviews')


# SCHEMAS:
class User(BaseModel):
    id: int
    name: str
    age: int
    nationality: str


class Game(BaseModel):
    id: int
    title: str
    genre: str
    price: int
    age_range: int


class Purchase(BaseModel):
    id: int
    game_id: int
    user_id: int
    price: int
    date: int


class Review(BaseModel):
    id: int
    game_id: int
    message: str
    rating: int
