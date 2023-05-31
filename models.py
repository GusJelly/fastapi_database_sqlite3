from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int
    nationality: str


class Game(BaseModel):
    id: int
    title: str
    genre: str
    number_of_players: int
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
