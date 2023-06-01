from fastapi import FastAPI
from models import GameCreate, UserCreate, PurchaseCreate, ReviewCreate

from database import (
    GameTable,
    UserTable,
    PurchaseTable,
    ReviewTable,
    Session,
    Base,
    engine
)


app = FastAPI()


# http requests:
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create database:  ===========================================================

@app.get("/setup/user")
async def setup_user():
    Base.metadata.create_all(engine)
    return "Table created"


@app.get("/setup/game")
async def setup_game():
    Base.metadata.create_all(engine)
    return "Table created"


@app.get("/setup/purchase")
async def setup_purchase():
    Base.metadata.create_all(engine)
    return "Table created"


@app.get("/setup/review")
async def setup_review():
    Base.metadata.create_all(engine)
    return "Table created"

#  ===========================================================================


# Post a new game
@app.post("/Game/post")
async def post_game(item: GameCreate):
    session = Session()
    game = GameTable(item.dict())
    session.add(game)
    session.commit()
    session.close()
    return "Item posted"


# Post a new user
@app.post("/User/post")
async def post_user(item: UserCreate):
    session = Session()
    user = UserTable(item.dict())
    session.add(user)
    session.commit()
    session.close()
    return "Item posted"


# Post a new purchase
@app.post("/Purchase/post")
async def post_purchase(item: PurchaseCreate):
    session = Session()
    purchase = PurchaseTable(item.dict())
    session.add(purchase)
    session.commit()
    session.close()
    return "Item posted"


# Post a new review
@app.post("/Review/post")
async def post_review(item: ReviewCreate):
    session = Session()
    review = ReviewTable(item.dict())
    session.add(review)
    session.commit()
    session.close()
    return ""
