from fastapi import FastAPI
import sqlite3
import logging
from models import GameTable, UserTable, PurchaseTable, ReviewTable

database_path = "online_game_shop.db"
con = sqlite3.connect(database_path)
cur = con.cursor()

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.DEBUG)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create database:
@app.get("/setup/user")
async def setup_user():
    cur.execute("""
        CREATE TABLE User(
            id INT PRIMARY KEY NOT NULL,
            name VARCHAR(100) NOT NULL,
            age INT,
            nationality VARCHAR(100)
        )
    """)
    con.commit()
    return "table created"


@app.get("/setup/game")
async def setup_game():
    cur.execute("""
        CREATE TABLE Game(
            id INT PRIMARY KEY NOT NULL,
            title VARCHAR(100),
            genre VARCHAR(100),
            price INT,
            age_range INT
        )
    """)
    con.commit()
    return "table created"


@app.get("/setup/purchase")
async def setup_purchase():
    cur.execute("""
        CREATE TABLE Purchase(
            id INT PRIMARY KEY NOT NULL,
            game_id INT NOT NULL,
            user_id INT NOT NULL,
            price INT,
            date INT,
            FOREIGN KEY(game_id) REFERENCES Game(id),
            FOREIGN KEY(user_id) REFERENCES User(id)
        )
    """)
    con.commit()
    return "table created"


@app.get("/setup/review")
async def setup_review():
    cur.execute("""
        CREATE TABLE Review(
            id INT PRIMARY KEY NOT NULL,
            user_id NOT NULL,
            game_id NOT NULL,
            message VARCHAR(100) NOT NULL,
            rating INT,
            FOREIGN KEY(user_id) REFERENCES User(id),
            FOREIGN KEY(game_id) REFERENCES Game(id)
        )
    """)


@app.get("/Gamer")
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


@app.post("/Game_posting")
async def post_game(item: GameTable):
    data = item.dict()
    query = """
        INSERT INTO Game (
            id,
            title,
            genre,
            number_of_players,
            price,
            age_range
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    cur.execute(query, (
        data['id'],
        data['title'],
        data['genre'],
        data['number_of_players'],
        data['price'],
        data['age_range']
    ))

    con.commit()
    return "Item posted"


@app.on_event("shutdown")
async def shutdown():
    con.close()
