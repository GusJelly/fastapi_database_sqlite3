from pydantic import BaseModel


class UserTable(BaseModel):
    id: int = None
    name: str
    age: int
    nationality: str


class GameTable(BaseModel):
    id: int = None
    title: str
    genre: str
    number_of_players: int = None
    price: int
    age_range: int


class PurchaseTable(BaseModel):
    id: int = None
    game_id: int
    user_id: int
    price: int
    date: int


class ReviewTable(BaseModel):
    id: int = None
    game_id: int
    message: str
    rating: int
