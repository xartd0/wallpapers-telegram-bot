import sqlite3
from tgbot.logger import logger

class Data:    
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        
    def create_user(self, user):
        with self.connection:
            self.cursor.execute("INSERT INTO bot_users VALUES (null, ?, ?, ?, ?, ?, ?)", (user))
            logger.info(f'User {user} added')

    def add_wallpaper(self, wallpaper):
        with self.connection:
            self.cursor.execute("INSERT INTO bot_wallpapers VALUES (null, ?, ?, ?, ?, ?)", (wallpaper))
            logger.info(f'Wallpaper {wallpaper} added')

    def take_wallpaper_by_id(self, id):
        with self.connection:
            self.cursor.execute("SELECT * FROM bot_wallpapers WHERE id = ?", (id,))
            return self.cursor.fetchall()

    def add_like(self, id, user_id):
        with self.connection:
            self.cursor.execute("UPDATE bot_wallpapers SET likes = likes + 1 WHERE id = ?", (id,))
            self.cursor.execute("INSERT INTO user_likes VALUES (?, ?)", (user_id, id))

    def remove_like(self, id, user_id):
        with self.connection:
            self.cursor.execute("UPDATE bot_wallpapers SET likes = likes - 1 WHERE id = ?", (id,))
            self.cursor.execute("DELETE FROM user_likes WHERE tg_id = ? and wall_id = ?", (user_id, id))

    def add_anti_id(self, anti_id, user_id):
        with self.connection:
            self.cursor.execute("UPDATE bot_users SET anti_id = ? WHERE tg_id = ?", (anti_id,user_id,))

    def check_user(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT name FROM bot_users WHERE tg_id = ?", (user_id,))
            return self.cursor.fetchone()

    def get_all_users(self):
        with self.connection:
            self.cursor.execute("SELECT count(*) FROM bot_users")
            return self.cursor.fetchone()[0]

    def get_user_likes(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT sum(likes) FROM bot_wallpapers WHERE owner_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def get_user_date(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT time_reg FROM bot_users WHERE tg_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def get_notif_user(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT notif FROM bot_users WHERE tg_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def change_notif_user(self, notif, user_id):
        with self.connection:
            self.cursor.execute("UPDATE bot_users SET notif = ? WHERE tg_id = ?", (notif,user_id,))

    def get_user_wallpapers(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT count(*) FROM bot_wallpapers WHERE owner_id = ?", (user_id,))
            return self.cursor.fetchone()[0]

    def get_all_ids(self):
        with self.connection:
            clear_ids = []
            for row in self.cursor.execute("SELECT id from bot_wallpapers ORDER by likes DESC"):
                clear_ids.append(row[0])
            return clear_ids

    def get_all_users_ids(self):
        with self.connection:
            clear_ids = []
            for row in self.cursor.execute("SELECT tg_id FROM bot_users"):
                clear_ids.append(row[0])
            return clear_ids

    def check_like(self, user_id, wall_id):
        with self.connection:
            self.cursor.execute("SELECT tg_id FROM user_likes WHERE tg_id = ? and wall_id = ?", (user_id,wall_id,))
            return self.cursor.fetchone()

    def count_wallpapers(self):
        with self.connection:
            self.cursor.execute("select count(*) from bot_wallpapers")
            return self.cursor.fetchone()[0]
