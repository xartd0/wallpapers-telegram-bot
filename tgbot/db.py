import sqlite3
from tgbot.logger import logger

class Data:    
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        
    def create_user(self, user):
        with self.connection:
            self.cursor.execute("INSERT INTO bot_users VALUES (null, ?, ?, ?, ?)", (user))
            logger.info(f'User {user} added')

    def add_wallpaper(self, wallpaper):
        with self.connection:
            self.cursor.execute("INSERT INTO bot_wallpapers VALUES (null, ?, ?, ?, ?, ?)", (wallpaper))
            logger.info(f'Wallpaper {wallpaper} added')
    
    def take_wallpaper(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM bot_wallpapers ORDER BY random() LIMIT 1")
            return self.cursor.fetchall()

    def take_wallpaper_by_id(self, id):
        with self.connection:
            self.cursor.execute("SELECT * FROM bot_wallpapers WHERE id = ?", (id,))
            return self.cursor.fetchall()

    def add_like(self, id):
        with self.connection:
            self.cursor.execute("UPDATE bot_wallpapers SET likes = likes + 1 WHERE id = ?", (id,))

    def add_user_likes(self, user_id, wall_id):
        with self.connection:
            self.cursor.execute("INSERT INTO user_likes VALUES (?, ?)", (user_id, wall_id))

    def check_user(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT name FROM bot_users WHERE tg_id = ?", (user_id,))
            return self.cursor.fetchone()

    def check_like(self, user_id, wall_id):
        with self.connection:
            self.cursor.execute("SELECT tg_id FROM user_likes WHERE tg_id = ? and wall_id = ?", (user_id,wall_id,))
            return self.cursor.fetchone()