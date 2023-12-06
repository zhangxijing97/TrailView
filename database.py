import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('trails.db')
        self.cursor = self.con.cursor()
        self.create_trail_table()

    '''CREATE the Trails TABLE'''
    # def create_trail_table(self):
    #     self.cursor.execute("CREATE TABLE IF NOT EXISTS trails(id integer PRIMARY KEY AUTOINCREMENT, trail varchar(50) NOT NULL, saved BOOLEAN NOT NULL CHECK (saved IN (0, 1)))")

    def create_trail_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trails(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trail VARCHAR(50) NOT NULL,
                            
                location TEXT,
                latitude REAL,
                longitude REAL,
                length REAL,
                difficulty TEXT,
                duration REAL,
                isKidFriendly BOOLEAN,
                isPetFriendly BOOLEAN,
                            
                saved BOOLEAN NOT NULL CHECK (saved IN (0, 1))
            )
        """)
    
    '''CREATE A Trail'''
    # def create_trail(self, trail):
    #     self.cursor.execute("INSERT INTO trails(trail, saved) VALUES(?, ?)", (trail, 0))
    #     self.con.commit()

    #     created_trail = self.cursor.execute("SELECT id, trail FROM trails WHERE trail = ? and saved = 0", (trail,)).fetchall()
    #     return created_trail[-1]

    def create_trail(self, trail, location=None, latitude=None, longitude=None, length=None, difficulty=None, duration=None, is_kid_friendly=None, is_pet_friendly=None):
        self.cursor.execute("""
            INSERT INTO trails(
                trail, location, latitude, longitude, length, difficulty, duration, isKidFriendly, isPetFriendly, saved
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (trail, location, latitude, longitude, length, difficulty, duration, is_kid_friendly, is_pet_friendly, 0))
        self.con.commit()

        created_trail = self.cursor.execute("SELECT id, trail FROM trails WHERE trail = ? and saved = 0", (trail,)).fetchall()
        return created_trail[-1]
    
    '''READ / GET the trails''' 
    # def get_trails(self):
    #     # Getting all saved and unsaved trails
    #     saved_trails = self.cursor.execute("SELECT id, trail FROM trails WHERE saved = 1").fetchall()
    #     unsaved_trails = self.cursor.execute("SELECT id, trail FROM trails WHERE saved = 0").fetchall()
    #     return saved_trails, unsaved_trails

    def get_trails(self):
        # Getting all trails, regardless of saved status
        all_trails = self.cursor.execute("SELECT id, trail, location, latitude, longitude, length, difficulty, duration, isKidFriendly, isPetFriendly, saved FROM trails").fetchall()
        return all_trails
    
    def get_saved_and_unsaved_trails(self):
        # Calling the get_all_trails method to get all trails
        all_trails = self.get_trails()

        # Separating saved and unsaved trails
        saved_trails = [trail for trail in all_trails if trail[0] == 1]
        unsaved_trails = [trail for trail in all_trails if trail[0] == 0]

        return saved_trails, unsaved_trails
    
    def get_saved_trails(self):
        saved_trails = self.cursor.execute("SELECT id, trail, location, latitude, longitude, length, difficulty, duration, isKidFriendly, isPetFriendly, saved FROM trails WHERE saved = 1").fetchall()
        return saved_trails
    
    def get_petFriendly_trails(self):
        petFriendly_trails = self.cursor.execute("SELECT id, trail, location, latitude, longitude, length, difficulty, duration, isKidFriendly, isPetFriendly, saved FROM trails WHERE isPetFriendly = 1").fetchall()
        return petFriendly_trails
    
    def get_filter_trails(self, query):
        print(query)
        petFriendly_trails = self.cursor.execute(query).fetchall()
        return petFriendly_trails
    
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
    
    def get_saved_status(self, trailid):
        saved_status = self.cursor.execute("SELECT saved FROM trails WHERE id=?", (trailid,)).fetchone()
        return bool(saved_status[0]) if saved_status else None

    '''Deleting the trail'''
    def delete_trail(self, trailid):
        self.cursor.execute("DELETE FROM trails WHERE id=?", (trailid,))
        self.con.commit()

    '''Closing the connection '''
    def close_db_connection(self):
        self.con.close()