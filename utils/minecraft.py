import mariadb
import os


class MinecraftManager:
    def __init__(self):
        USER = os.environ.get('MC_USER')
        PASSWORD = os.environ.get('MC_PASSWORD')
        HOST = os.environ.get('MC_HOST')
        PORT = int(os.environ.get('MC_PORT'))
        DATABASE = os.environ.get('MC_DATABASE')

        self.conn = mariadb.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE,
        )

        self.conn.auto_reconnect = True
        self.cur = self.conn.cursor()

    def is_code_valid(self, code):
        self.cur.execute("SELECT COUNT(1) FROM code WHERE code = ?", (code, ))
        return 1 in self.cur.fetchall()[0]

    def is_player_whitelisted(self, code):
        self.cur.execute("SELECT whitelisted FROM player WHERE uuid IN (SELECT player_uuid FROM code WHERE code = ?)", (code, ))
        return 1 in self.cur.fetchall()[0]

    def whitelist_player(self, code):
        self.cur.execute("UPDATE player SET whitelisted = 1 WHERE uuid IN (SELECT player_uuid FROM code WHERE code = ?)", (code, ))
        self.bot.conn.commit()

    
            
