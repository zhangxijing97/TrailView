import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('trails.db')
        self.cursor = self.con.cursor()
        self.create_trail_table()

    '''CREATE the Trails TABLE'''
    def create_trail_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS trails(id integer PRIMARY KEY AUTOINCREMENT, trail varchar(50) NOT NULL, due_date varchar(50), saved BOOLEAN NOT NULL CHECK (saved IN (0, 1)))")
    
    '''CREATE A Trail'''
    def create_trail(self, trail, due_date=None):
        self.cursor.execute("INSERT INTO trails(trail, due_date, saved) VALUES(?, ?, ?)", (trail, due_date, 0))
        self.con.commit()

        created_trail = self.cursor.execute("SELECT id, trail, due_date FROM trails WHERE trail = ? and saved = 0", (trail,)).fetchall()
        return created_trail[-1]
    
    '''READ / GET the trails''' 
    def get_trails(self):
        # Getting all saved and unsaved trails
        saved_trails = self.cursor.execute("SELECT id, trail, due_date FROM trails WHERE saved = 1").fetchall()
        unsaved_trails = self.cursor.execute("SELECT id, trail, due_date FROM trails WHERE saved = 0").fetchall()
        return saved_trails, unsaved_trails

    '''UPDATING the trails status'''
    def mark_trail_as_saved(self, trailid):
        self.cursor.execute("UPDATE trails SET saved=1 WHERE id=?", (trailid,))
        self.con.commit()
    
    def mark_trail_as_unsaved(self, trailid):
        self.cursor.execute("UPDATE trails SET saved=0 WHERE id=?", (trailid,))
        self.con.commit()

        # returning the trail text
        trail_text = self.cursor.execute("SELECT trail FROM trails WHERE id=?", (trailid,)).fetchall()
        return trail_text[0][0]

    '''Deleting the trail'''
    def delete_trail(self, trailid):
        self.cursor.execute("DELETE FROM trails WHERE id=?", (trailid,))
        self.con.commit()

    '''Closing the connection '''
    def close_db_connection(self):
        self.con.close()