import os
import sqlite3
from random import randint
from dotenv import load_dotenv
from assets.scripts.date import now
from assets.scripts.terminal import colors as tc

class DatabaseInterface:
    def __init__(self, database_path):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.database = database_path

    def execute(self, query, data):
        self.cur.execute(query, data)
        self.conn.commit()
        return self.cur

    def add_user(self, username, usertag, userid):
        self.cur.execute("INSERT INTO users VALUES(?,?,?)", (username, usertag, userid))
        self.conn.commit()
        print(f"{now()} {tc.fg.green}DATABASE     {tc.reset}INSERT INTO users VALUES({username},{usertag},{userid})")
        return self.cur

    def fetch_user(self, id=None):
        self.cur.execute("SELECT userid FROM users WHERE userid=(?)", (id,))
        result = self.cur.fetchone()

        if result:
            return result
        return False

    def random_user(self):
        self.cur.execute("SELECT COUNT(*) FROM users")

        totalrows = self.cur.fetchone()
        randomrow = randint(1, int(totalrows[0]))

        self.cur.execute("SELECT userid FROM users WHERE rowid=(?)", (randomrow,))
        result = self.cur.fetchone()
        return result


    def add_guild(self, id, prefix):
        self.cur.execute("INSERT INTO guilds VALUES(?,?)", (id, prefix))
        print(f"{now()} {tc.fg.green}DATABASE     {tc.reset}INSERT INTO guilds VALUES({id},{prefix}")
        self.conn.commit()
        return self.cur

    def delete_guild(self, guild_id):
        self.cur.execute("DELETE FROM guilds WHERE id = (?)", (guild_id,))
        print(f"{now()} {tc.fg.green}DATABASE     {tc.reset}DELETE FROM guilds WHERE id = ({guild_id})")
        self.conn.commit()
        return self.cur

    def fetch_prefix(self, guild_id):
        self.cur.execute("SELECT prefix FROM guilds WHERE id = (?)", (guild_id,))
        prefix = self.cur.fetchone()

        return prefix

    def change_prefix(self, guild_id, prefix):
        self.cur.execute("""UPDATE guilds
                            SET prefix = (?)
                            WHERE
                                id = (?)""", (prefix, guild_id))

        print(f"{now()} {tc.fg.green}DATABASE     {tc.reset}UPDATE guilds SET prefix = {prefix} WHERE id = {guild_id}")
        self.conn.commit()
        return self.cur

    def databaseStatus(self):
        try:
            self.cur
            return "Online"
        except Exception as ex:
            return "Offline" 

    def __del__(self):
        """ Destroys instance and connection on completion of called method """
        self.conn.close()


def CreateTables(db_interface, table):
    f = open(table)
    full_sql = f.read() 
    sql_commands = full_sql.replace('\n', '').split(';')[:-1]
    for sql_command in sql_commands: 
        db_interface.cur.execute(sql_command) 

    f.close()



load_dotenv()
if os.path.exists(os.getenv("DATABASE")):
    print(os.path.exists(os.getenv("DATABASE")))
    DB = DatabaseInterface(os.getenv("DATABASE"))
else:
    DB = DatabaseInterface(os.getenv("DATABASE"))
    CreateTables(DB, "./database/schema.sql")
