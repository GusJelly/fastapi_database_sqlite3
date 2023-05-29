from fastapi import FastAPI
import sqlite3

database_path = "./online_game_shop.db"
con = sqlite3.connect(database_path)
cur = con.cursor()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/insert_games")
async def insert_games(title: str, genre: str, price: int, age_range: int):
    query = f"""
        INSERT INTO Game(title, genre, price, age_range)
        VALUES({title}, {genre}, {price}, {age_range})
    """
    cur.execute(query)
    con.commit()

    return {"Query completed"}


# this closes the connection to the database made with sqlite3
@app.on_event("shutdown")
async def shutdown():
    con.close()
