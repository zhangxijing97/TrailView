import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('trails.db')
        self.cursor = self.con.cursor()
        self.create_trail_table()

    def create_trail_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS trails(id integer PRIMARY KEY AUTOINCREMENT, trail varchar(50) NOT NULL, saved BOOLEAN NOT NULL CHECK (saved IN (0, 1)))")

    def create_trail(self, trail):
        self.cursor.execute("INSERT INTO trails(trail, saved) VALUES(?, ?)", (trail, 0))
        self.con.commit()
        created_trail = self.cursor.execute("SELECT id, trail FROM trails WHERE trail = ? and saved = 0", (trail,)).fetchall()
        return created_trail[-1]

    def get_trails(self):
        saved_trails = self.cursor.execute("SELECT id, trail FROM trails WHERE saved = 1").fetchall()
        unsaved_trails = self.cursor.execute("SELECT id, trail FROM trails WHERE saved = 0").fetchall()
        return saved_trails, unsaved_trails

    def mark_trail_as_saved(self, trailid):
        self.cursor.execute("UPDATE trails SET saved=1 WHERE id=?", (trailid,))
        self.con.commit()

    def mark_trail_as_unsaved(self, trailid):
        self.cursor.execute("UPDATE trails SET saved=0 WHERE id=?", (trailid,))
        self.con.commit()
        trail_name = self.cursor.execute("SELECT trail FROM trails WHERE id=?", (trailid,)).fetchall()
        return trail_name[0][0]

    def delete_trail(self, trailid):
        self.cursor.execute("DELETE FROM trails WHERE id=?", (trailid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()