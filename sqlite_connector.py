import sqlite3

con = sqlite3.connect("online_game_shop.db")

cur = con.cursor()


cur.execute('''
            CREATE TABLE Game(
                id int NOT NULL,
                title varchar(50),
                genre varchar(50),
                number_of_players int,
                price double,
                age_range int,
                PRIMARY KEY(id)
                );
            ''')


cur.execute('''
            CREATE TABLE Gamer(
                id int PRIMARY KEY NOT NULL,
                name varchar(50),
                age int,
                nationality varchar(50)
                );
            ''')


cur.execute('''
            CREATE TABLE Review (
                id int NOT NULL,
                gamer_id int,
                game_id int,
                message varchar(200),
                rating int,
                PRIMARY KEY(id),
                FOREIGN KEY(gamer_id) REFERENCES Gamer(id)
                );
            ''')


cur.execute('''
            CREATE TABLE Purchase (
                id int NOT NULL,
                gamer_id int,
                game_id int,
                price int,
                purchase_date varchar(10),
                PRIMARY KEY(id),
                FOREIGN KEY(gamer_id) REFERENCES Gamer(id),
                FOREIGN KEY(game_id) REFERENCES Game(id)
                );
            ''')
