import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    # users
    def add_user(self, user_id):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("INSERT INTO user_id (id) VALUES (?)", (user_id,))
            
        self.connection.commit()
        self.connection.close()

    def user_exists(self, user_id):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            result = self.cursor.execute("SELECT id FROM user_id WHERE id = ?", (user_id,)).fetchall()

        self.connection.close()
        return bool(len(result))

    def del_user(self, user_id):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("DELETE FROM user_id WHERE id = ?", (user_id,))
            
        self.connection.commit()
        self.connection.close()

    def all_users(self):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            result = self.cursor.execute("SELECT id FROM user_id").fetchall()

        self.connection.close()
        return result
    
    # comments
    def view_comments(self):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            result = self.cursor.execute("SELECT * FROM comment").fetchall()

        self.connection.close()
        return result

    def add_comment(self, comment_name, comment_text):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("INSERT INTO comment (name, text) VALUES (?, ?)", (comment_name, comment_text,))
            
        self.connection.commit()
        self.connection.close()
    
    def edit_comment_name(self, id_comment, comment_name):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("UPDATE comment SET name = ? WHERE id_comment = ?", (comment_name, id_comment,))
                
        self.connection.commit()
        self.connection.close()
    
    def edit_comment_text(self, id_comment, comment_text):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("UPDATE comment SET text = ? WHERE id_comment = ?", (comment_text, id_comment,))
                
        self.connection.commit()
        self.connection.close()
    
    def del_comment(self, id_comment):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("DELETE FROM comment WHERE id_comment = ?", (id_comment,))

        self.connection.commit()
        self.connection.close()
    