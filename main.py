from fastapi import FastAPI
import sqlite3
import logging

database_path = "./online_game_shop.db"
con = sqlite3.connect(database_path)
cur = con.cursor()

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.DEBUG)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/Gamer/")
async def gamer(name: str, age: int = 0, nationality: str = "portugal"):
    query = f"""
        SELECT * FROM Gamer WHERE name = {name};
    """
    try:
        cur.execute(query, (name))
        query_data = cur.fetchone()

        if query_data:
            return {
                "name": query_data[1],
                "age": query_data[2],
                "nationality": query_data[3]
            }
        else:
            return {"message": "Gamer not found"}
    except Exception as e:
        logging.error(f"Error retrieving gamer: {e}")
        return {"message": "Internal server error"}


@app.post("/insert_game/")
async def insert_game(
    id: int,
    title: str,
    genre: str,
    price: int = 60,
    age_range: int = 18
):
    query = f"""
        INSERT INTO Game(id, title, genre, price, age_range)
        VALUES({id}, {title}, {genre}, {price}, {age_range})
    """
    try:
        cur.execute(query, (title, genre, price, age_range))
        con.commit()
        return {"message": "Game inserted successfully"}
    except Exception as e:
        logging.error(f"Error inserting game: {e}")
        return {"message": "Internal server error"}


@app.post("/insert_gamer/")
async def insert_gamer(
    id: int,
    name: str,
    nationality: str,
    age: int = 0
):
    query = f"""
        INSERT INTO Gamer (id, name, age, nationality)
        VALUES({id}, {name}, {nationality}, {age});
    """
    try:
        cur.execute(query, (name, age, nationality))
        con.commit()
        return {"message": "Gamer inserted successfully"}
    except Exception as e:
        logging.error(f"Error inserting gamer: {e}")
        return {"message": "Internal server error"}


@app.post("/insert_purchase/")
async def insert_purchase(
    id: int,
    gamer_id: int,
    game_id: int,
    price: int,
    purchase_date: str
):
    query = f"""
        INSERT INTO Purchase (id, gamer_id, game_id, price, purchase_date)
        VALUES({id}, {gamer_id}, {game_id}, {price}, {purchase_date})
    """
    try:
        cur.execute(query, (gamer_id, game_id, price, purchase_date))
        con.commit()
        return {"message": "Purchase inserted successfully"}
    except Exception as e:
        logging.error(f"Error inserting purchase: {e}")
        return {"message": "Internal server error"}


@app.post("/insert_review/")
async def insert_review(
    id: int,
    gamer_id: int,
    game_id: int,
    message: str,
    rating: int
):
    query = f"""
        INSERT INTO Review (id, gamer_id, game_id, message, rating)
        VALUES({id}, {gamer_id}, {game_id}, {message}, {rating})
    """
    try:
        cur.execute(query, (gamer_id, game_id, message, rating))
        con.commit()
        return {"message": "Review inserted successfully"}
    except Exception as e:
        logging.error(f"Error inserting review: {e}")
        return {"message": "Internal server error"}


@app.on_event("shutdown")
async def shutdown():
    con.close()
