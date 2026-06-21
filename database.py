import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("user_info.db")
        self.cursor = self.conn.cursor()

        self.create_table()
        self.create_admin()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER,
            favourite_game TEXT,
            role TEXT DEFAULT 'user'
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores(
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            game_name TEXT,
            score INTEGER,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
        """)

        self.conn.commit()

    def register_user(self,username,password,age,favourite_game,role="user"):

        try:
            self.cursor.execute("""INSERT INTO users(username,password,age,favourite_game,role)VALUES(?,?,?,?,?)""",(username,password,age,favourite_game,role))
            self.conn.commit()

            return True

        except sqlite3.IntegrityError:

            return False

    def login_user(self, username, password):

        self.cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """, (username, password))

        return self.cursor.fetchone()

    def user_exists(self, username):

        self.cursor.execute("""
        SELECT * FROM users
        WHERE username=?
        """, (username,))

        return self.cursor.fetchone()

    def create_admin(self):

        self.cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
        """, ("Admin1",))

        admin = self.cursor.fetchone()

        if admin is None:
            self.cursor.execute("""
            INSERT INTO users(
                username,
                password,
                age,
                favourite_game,
                role
            )
            VALUES(?,?,?,?,?)
            """, (
                "Admin1",
                "Admin@123",
                0,
                "None",
                "admin"
            ))

        self.conn.commit()

        self.cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
        """, ("Admin2",))

        admin = self.cursor.fetchone()

        if admin is None:
            self.cursor.execute("""
            INSERT INTO users(
                username,
                password,
                age,
                favourite_game,
                role
            )
            VALUES(?,?,?,?,?)
            """, (
                "Admin2",
                "Admin@456",
                0,
                "None",
                "admin"
            ))

        self.conn.commit()

    def save_score(self, user_id, game_name, score):
        self.cursor.execute("""
            INSERT INTO scores (user_id, game_name, score)
            VALUES (?, ?, ?)
        """, (user_id, game_name, score))
        self.conn.commit()


    def get_user_high_scores(self, user_id):
        self.cursor.execute("""
            SELECT game_name, MAX(score)
            FROM scores
            WHERE user_id = ?
            GROUP BY game_name
        """, (user_id,))
        return self.cursor.fetchall()


    def get_all_high_scores(self):
        self.cursor.execute("""
            SELECT users.username, scores.game_name, MAX(scores.score)
            FROM scores
            JOIN users ON users.id = scores.user_id
            GROUP BY users.username, scores.game_name
            """)
        return self.cursor.fetchall()

    def get_total_users(self):

        self.cursor.execute(
        "SELECT COUNT(*) FROM users WHERE role = 'user'"
        )

        return self.cursor.fetchone()[0]

    def get_total_games_played(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM scores"
        )

        return self.cursor.fetchone()[0]

    def get_average_score(self):

        self.cursor.execute(
            "SELECT AVG(score) FROM scores"
        )

        avg = self.cursor.fetchone()[0]

        if avg is None:
            return 0

        return round(avg,2)

    def get_game_statistics(self):

        self.cursor.execute("""
        SELECT game_name,
        COUNT(*)
        FROM scores
        GROUP BY game_name
        """)

        return self.cursor.fetchall()

    def get_best_score_per_game(self):

        self.cursor.execute("""
        SELECT game_name, MAX(score)
        FROM scores
        GROUP BY game_name
        """)

        return self.cursor.fetchall()

    def get_game_high_scores(self):
        """Fetches the maximum score achieved across all users for each game."""
        self.cursor.execute("""
            SELECT game_name, MAX(score)
            FROM scores
            GROUP BY game_name
        """)
        return self.cursor.fetchall()

    def get_user_profile(self, user_id):

        self.cursor.execute("""
            SELECT username, age, favourite_game
            FROM users
            WHERE id = ?
        """, (user_id,))

        return self.cursor.fetchone()

    def get_games_played(self, user_id):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM scores
            WHERE user_id = ?
        """, (user_id,))

        return self.cursor.fetchone()[0]
