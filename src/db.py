import sqlite3

class Database():
    
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
        
    def get_badwords(self):
        with self.connection:
            res= self.cursor.execute("SELECT * FROM words").fetchall()
            if res== []:
                return None
            else:
                return res
        
    def add_badwords(self, word):
        with self.connection:
            return self.cursor.execute("INSERT INTO words (bad_words) VALUES (?)", (word, )).fetchall()
        
    def del_badwords(self, word):
        with self.connection:
            return self.cursor.execute("DELETE FROM words WHERE bad_words= ?", (word, ))
    
    def del_post(self, key):
        with self.connection:
            return self.cursor.execute("DELETE FROM suspicious WHERE key= ?", (key, ))
   
    def get_post(self, key):
        with self.connection:
            return self.cursor.execute("SELECT * FROM suspicious WHERE key= ?", (key, )).fetchone()
        
    def add_post(self, key, owner_id, post_id, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO suspicious (key, owner_id, post_id, user_id) VALUES (?,?,?,?)", (key, owner_id, post_id, user_id,))

    def words_exist(self, word):
        with self.connection:
            res= self.cursor.execute("SELECT COUNT(bad_words) FROM words WHERE bad_words= ?", (word,)).fetchone()
            return bool(res[0])