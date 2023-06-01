from pydantic import BaseModel
from typing import Optional


# SCHEMAS:
class UserCreate(BaseModel):
    id: Optional[int]  # O Optional deixa a base de dados lidar com os ids
    name: str
    age: int
    nationality: str


class GameCreate(BaseModel):
    id: Optional[int]
    title: str
    genre: str
    price: int
    age_range: int


class PurchaseCreate(BaseModel):
    id: Optional[int]
    game_id: int
    user_id: int
    price: int
    date: int


class ReviewCreate(BaseModel):
    id: Optional[int]
    game_id: int
    message: str
    rating: int
