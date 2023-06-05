from pydantic import BaseModel
from typing import Optional


# SCHEMAS:
class User(BaseModel):
    id: Optional[int]  # O Optional deixa a base de dados lidar com os ids
    name: str
    age: int
    nationality: str


class Game(BaseModel):
    id: Optional[int]
    title: str
    genre: str
    price: int
    age_range: int


class Purchase(BaseModel):
    id: Optional[int]
    game_id: int
    user_id: int
    price: int
    date: int


class Review(BaseModel):
    id: Optional[int]
    game_id: int
    message: str
    rating: int
