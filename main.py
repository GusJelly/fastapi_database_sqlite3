from fastapi import FastAPI
import sqlite3
from models import Game, User, Purchase, Review

# Create connection to database file:
database_path = "online_game_shop.db"
con = sqlite3.connect(database_path)
cur = con.cursor()

app = FastAPI()


# http requests:
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create database:
@app.post("/setup/user")
async def setup_user(item: User):
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


@app.post("/Game/post")
async def post_game(item: Game):
    data = item.dict()
    query = """
        INSERT INTO Game (
            id,
            title,
            genre,
            price,
            age_range
        )
        VALUES (?, ?, ?, ?, ?)
    """

    cur.execute(query, (
        data['id'],
        data['title'],
        data['genre'],
        data['price'],
        data['age_range']
    ))

    con.commit()
    return "Item posted"


@app.post("/User/post")
async def post_user(item: User):
    data = item.dict()
    query = """
        INSERT INTO User (
            id,
            name,
            age,
            nationality
        )
        VALUES (?, ?, ?, ?)
    """

    cur.execute(query, (
        data['id'],
        data['name'],
        data['age'],
        data['nationality']
    ))

    con.commit()
    return "Item posted"


@app.post("/Purchase/post")
async def post_purchase(item: Purchase):
    data = item.dict()
    query = """
        INSERT INTO Purchase (
            id,
            game_id,
            user_id,
            price,
            date
        )
        VALUES (?, ?, ?, ?, ?)
    """

    cur.execute(query, (
        data['id'],
        data['game_id'],
        data['user_id'],
        data['price'],
        data['date']
    ))

    con.commit()
    return "Item posted"


@app.post("/Review/post")
async def post_review(item: Review):
    data = item.dict()
    query = """
        INSERT INTO Review (
            id,
            game_id,
            message,
            rating
        )
        VALUES (?, ?, ?, ?)
    """

    cur.execute(query, (
        data['id'],
        data['game_id'],
        data['message'],
        data['rating']
    ))

    con.commit()
    return ""


@app.on_event("shutdown")
async def shutdown():
    con.close()
