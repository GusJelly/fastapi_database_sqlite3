from fastapi import FastAPI
import sqlite3
from models import Game, User, Purchase, Review

# Create connection to database file:
database_path = "online_game_shop.db"
con = sqlite3.connect(database_path)  # conexao a base de dados
cur = con.cursor()  # cursor é um ponteiro para uma posicao especifica na base de daodos

app = FastAPI()


# http requests:
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create database:  ===========================================================

# id INTEGER PRIMARY KEY NOT NULL <- isto faz com que os id's
    # auto incrementem com cada entrada;

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

    cur.execute(query, (name,))  # tem mesmo de ser (name,) para ser uma lista de argumentos

    query_data = cur.fetchone()

    if query_data:
        return {
                "name": query_data[1],
                "age": query_data[2],
                "nationality": query_data[3]
                }
    else:
        return {"message": "Gamer not found"}


# pesquisar o jogo por ID
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
        return {"message": "Game not found"}

# pesquisar uma review por id
@app.get("/Review")
async def get_review(id: int):

    query = """
        SELECT * FROM Game WHERE id = ?;
    """
    cur.execute(query, (id,))
    query_data = cur.fetchone()

    if query_data:
        return {
                "user_id": query_data[1],
                "game_id": query_data[2],
                "message": query_data[3],
                "rating": query_data[4]
                }
    else:
        return {"message": "Review not found"}

# pesquisar uma purchase por id
@app.get("/Review")
async def get_purchase(id: int):

    query = """
        SELECT * FROM Game WHERE id = ?;
    """
    cur.execute(query, (id,))
    query_data = cur.fetchone()

    if query_data:
        return {
                "game_id": query_data[1],
                "user_id": query_data[2],
                "price": query_data[3],
                "date": query_data[4]
                }
    else:
        return {"message": "Purchase not found"}



# Post endpoints:  ============================================================


# Post a new game into the Game table:
@app.post("/Game/post")
async def insert_game(item: Game):
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
async def insert_user(item: User):
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
async def insert_purchase(item: Purchase):
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
async def insert_review(item: Review):
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


# update da tabela game
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


# update da tabela user
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


# TODO fazer um update apenas de um campo

@app.put("/User/update/{user_id}/{update_camp}")
async def update_one_user(user_id: int,
                          update_camp: str,
                          item: User):
    data = item.dict()
    query = f"""
        UPDATE User
        SET {update_camp} = ?
        WHERE id = ?
    """

    cur.execute(query, (
        data[update_camp],
        user_id
    ))

    con.commit()
    return "Item updated"


# Update one camp of Game table:
@app.put("/Game/update/{game_id}/{update_camp}")
async def update_one_game(game_id: int,
                          update_camp: str,
                          item: Game):
    data = item.dict()
    query = f"""
        UPDATE Game
        SET {update_camp} = ?
        WHERE id = ?
    """

    cur.execute(query, (
        data[update_camp],
        game_id
    ))

    con.commit()
    return "Item updated"


# Update one camp of Purchase table:
@app.put("/Purchase/update/{purchase_id}/{update_camp}")
async def update_one_purchase(purchase_id: int,
                              update_camp: str,
                              item: Purchase):
    data = item.dict()
    query = f"""
        UPDATE Purchase
        SET {update_camp} = ?
        WHERE id = ?
    """

    cur.execute(query, (
        data[update_camp],
        purchase_id
    ))

    con.commit()
    return "Item updated"


# Update one camp of Review table:
@app.put("/Review/update/{review_id}/{update_camp}")
async def update_one_review(review_id: int,
                            update_camp: str,
                            item: Review):
    data = item.dict()
    query = f"""
        UPDATE User
        SET {update_camp} = ?
        WHERE id = ?
    """

    cur.execute(query, (
        data[update_camp],
        review_id
    ))

    con.commit()
    return "Item updated"

#Delete de um jogo
@app.delete("/Game/delete/{game_id}")
async def delete_one_game(game_id: int,
                          item: Game):
    data = item.dict()
    query = f"""
        DELETE FROM Game
        WHERE id = ?
    """

    cur.execute(query, (game_id,))

    con.commit()
    return "Item updated"

#Delete de um user
@app.delete("/User/delete/{user_id}")
async def delete_one_user(user_id: int,
                          item: User):
    data = item.dict()
    query = f"""
        DELETE FROM User
        WHERE id = ?
    """

    cur.execute(query, (user_id,))

    con.commit()
    return "Item updated"

#Delete de uma review
@app.delete("/Review/delete/{review_id}")
async def delete_one_review(review_id: int,
                          item: Review):
    data = item.dict()
    query = f"""
        DELETE FROM Review
        WHERE id = ?
    """

    cur.execute(query, (review_id,))

    con.commit()
    return "Item updated"

#Delete de uma purchase
@app.delete("/Purchase/delete/{purchase_id}")
async def delete_one_purchase(purchase_id: int,
                          item: Purchase):
    data = item.dict()
    query = f"""
        DELETE FROM Purchase
        WHERE id = ?
    """

    cur.execute(query, (purchase_id,))

    con.commit()
    return "Item updated"

#  ===========================================================================


# shutdown the database connection:
@app.on_event("shutdown")
async def shutdown():
    con.close()