from fastapi import FastAPI
import sqlite3

database_path = "./online_game_shop.db"
con = sqlite3.connect(database_path)
cur = con.Cursor()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# this closes the connection to the database made with sqlite3
@app.on_event("shutdown")
async def shutdown():
    con.close()
