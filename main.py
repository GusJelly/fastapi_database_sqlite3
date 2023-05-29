from fastapi import FastAPI
import sqlite3

database_path = "./online_game_shop.db"
con = sqlite3.connect(database_path)
cur = con.cursor()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/insert_game")
async def insert_game(
        title: str,
        genre: str,
        price: int = 60,
        age_range: int = 18
        ):

    query = f"""
        INSERT INTO Game(title, genre, price, age_range)
        VALUES({title}, {genre}, {price}, {age_range})
    """
    cur.execute(query)
    con.commit()
    return {"Query completed"}


@app.post("/insert_gamer")
async def insert_gamer(
        name: str,
        nationality: str,
        age: int = 0
        ):
    query = f"""
        INSERT INTO Gamer (name, age, nationality)
        VALUES({name}, {age}, {nationality});
    """
    cur.execute(query)
    con.commit()
    return {"Query completed"}


@app.post("/insert_purchase")
async def insert_purchase(
        gamer_id: int,
        game_id: int,
        price: int,
        purchase_date: str
        ):
    query = f"""
        INSERT INTO Purchase (gamer_id, game_id, price, purchase_date)
        VALUES({gamer_id}, {game_id}, {price}, {purchase_date})
    """
    cur.execute(query)
    con.commit()
    return {"Query completed"}


@app.post("/insert_review")
async def insert_review(
        gamer_id: int,
        game_id: int,
        message: str,
        rating: int
        ):
    query = f"""
        INSERT INTO Review (gamer_id, game_ind, message, rating)
        VALUES({gamer_id}, {game_id}, {message}, {rating})
    """
    cur.execute(query)
    con.commit()
    return {"Query completed"}


# this closes the connection to the database made with sqlite3
@app.on_event("shutdown")
async def shutdown():
    con.close()
