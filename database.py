from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the database engine
engine = create_engine("sqlite:///online_game_shop.db")

# Create the base class for declarative models:
Base = declarative_base()

Session = sessionmaker(bind=engine)


# Define the Game model:
class GameTable(Base):
    __tablename__ = 'Game'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100))
    genre = Column(String(100))
    price = Column(Integer)
    age_range = Column(Integer)

    # Relationship with Purchase model
    purchases = relationship("Purchase", back_populates="game")
    # Relationship with Review model
    reviews = relationship("Review", back_populates="game")


# Define the User model:
class UserTable(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    nationality = Column(String(100))

    # Relationship with Purchase model
    purchases = relationship("Purchase", back_populates="user")
    # Relationship with Review model
    reviews = relationship("Review", back_populates="user")


# Define the Purchase model:
class PurchaseTable(Base):
    __tablename__ = 'Purchase'

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey('Game.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    price = Column(Integer)
    date = Column(Integer)

    # Relationship with Game model
    game = relationship("Game", back_populates="purchases")
    # Relationship with User model
    user = relationship("User", back_populates="purchases")


# Define the Review model:
class ReviewTable(Base):
    __tablename__ = 'Review'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('Game.id'), nullable=False)
    message = Column(String(100), nullable=False)
    rating = Column(Integer)

    # Relationship with User model
    user = relationship("User", back_populates="reviews")
    # Relationship with Game model
    game = relationship("Game", back_populates="reviews")


# Create the tables in the database:
Base.metadata.create_all(engine)
