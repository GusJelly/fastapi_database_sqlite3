from fastapi import FastAPI
import sqlite3
from models import Game, User, Purchase, Review

# Create connection to database file:
database_path = "online_game_shop.db"
con = sqlite3.connect(database_path) #conexao a base de dados
cur = con.cursor() #cursor é um ponteiro para uma posicao especifica na base de daodos

app = FastAPI()


# http requests:
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create database:  ===========================================================

# id INTEGER PRIMARY KEY NOT NULL <- isto faz com que os id's
    # auto incrementem com cada entrada;

#TODO alterar para post a criçao das tabelas
@app.post("/setup/user")
async def setup_user():
    cur.execute("""
        CREATE TABLE User(
            id INTEGER PRIMARY KEY NOT NULL,
            name VARCHAR(100) NOT NULL,
            age INT,
            nationality VARCHAR(100)
        )
    """)
    con.commit()
    return "table created"


@app.post("/setup/game")
async def setup_game():
    cur.execute("""
        CREATE TABLE Game(
            id INTEGER PRIMARY KEY NOT NULL,
            title VARCHAR(100),
            genre VARCHAR(100),
            price INT,
            age_range INT
        )
    """)
    con.commit()
    return "table created"


@app.post("/setup/purchase")
async def setup_purchase():
    cur.execute("""
        CREATE TABLE Purchase(
            id INTEGER PRIMARY KEY NOT NULL,
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


@app.post("/setup/review")
async def setup_review():

    cur.execute("""
        CREATE TABLE Review(
            id INTEGER PRIMARY KEY NOT NULL,
            user_id NOT NULL,
            game_id NOT NULL,
            message VARCHAR(100) NOT NULL,
            rating INT,
            FOREIGN KEY(user_id) REFERENCES User(id),
            FOREIGN KEY(game_id) REFERENCES Game(id)
        )
    """)
    con.commit()
    return {"Table Created"}
# ============================================================================


# Pesquisar por um User por nome:
@app.get("/User")
async def get_gamer(name: str):

    query = """
        SELECT * FROM User WHERE name = ?
    """

    cur.execute(query, (name,)) #tem mesmo de ser (name,) para ser uma lista de argumentos

    query_data = cur.fetchone()

    if query_data:
        return {
                "name": query_data[1],
                "age": query_data[2],
                "nationality": query_data[3]
                }
    else:
        return {"message": "Gamer not found"}

#pesquisar o jogo por ID
@app.get("/Game")
async def get_game(id: int):

    query = """
        SELECT * FROM Game WHERE id = ?;
    """
    cur.execute(query, (id,))
    query_data = cur.fetchone()

    if query_data:
        return {
                "title": query_data[1],
                "genre": query_data[2],
                "price": query_data[3],
                "age_range": query_data[4]
                }
    else:
        return {"message": "Gamer not found"}

#TODO get_Purchase e get_Review

# Post endpoints:  ============================================================

# Post a new game into the Game table:
@app.post("/Game/post")
async def create_game(item: Game):
    data = item.dict()
    query = """
        INSERT INTO Game (
            title,
            genre,
            price,
            age_range
        )
        VALUES (?, ?, ?, ?) 
    """
    # ? sao place holders

    cur.execute(query, (
        data['title'],
        data['genre'],
        data['price'],
        data['age_range']
    ))

    con.commit()
    return "Item posted"


# Post a new user into the User table:
@app.post("/User/post")
async def create_user(item: User):
    data = item.dict()
    query = """
        INSERT INTO User (
            name,
            age,
            nationality
        )
        VALUES (?, ?, ?)
    """

    cur.execute(query, (
        data['name'],
        data['age'],
        data['nationality']
    ))

    con.commit()
    return "Item posted"


# Post a new purchase into the purchase table:
@app.post("/Purchase/post")
async def create_purchase(item: Purchase):
    data = item.dict()
    query = """
        INSERT INTO Purchase (
            game_id,
            user_id,
            price,
            date
        )
        VALUES (?, ?, ?, ?)
    """

    cur.execute(query, (
        data['game_id'],
        data['user_id'],
        data['price'],
        data['date']
    ))

    con.commit()
    return "Item posted"


# Post a new review into the review table:
@app.post("/Review/post")
async def create_review(item: Review):
    data = item.dict()
    query = """
        INSERT INTO Review (
            game_id,
            message,
            rating
        )
        VALUES (?, ?, ?)
    """

    cur.execute(query, (
        data['game_id'],
        data['message'],
        data['rating']
    ))

    con.commit()
    return ""

#update da tabela game
@app.put("/Game/update/{id}")
async def update_game(id: int, item: Game):
    data = item.dict()
    query = """
        UPDATE Game
        SET title = ?,
            genre = ?,
            price = ?,
            age_range = ?
        WHERE id = ?
    """

    cur.execute(query, (
        data['title'],
        data['genre'],
        data['price'],
        data['age_range'],
        id
    ))

    con.commit()
    return "Item updated"

#update da tabela user
@app.put("/User/update/{user_id}")
async def update_user(user_id: int, item: User):
    data = item.dict()
    query = """
        UPDATE User
        SET name = ?,
            age = ?,
            nationality = ?
        WHERE id = ?
    """

    cur.execute(query, (
        data['name'],
        data['age'],
        data['nationality'],
        user_id
    ))

    con.commit()
    return "Item updated"

#TODO fazer um update apenas de um campo



#  ===========================================================================


# shutdown the database connection:
@app.on_event("shutdown")
async def shutdown():
    con.close()
