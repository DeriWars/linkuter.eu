from sqlite3 import *

class Database():
    """
    The url database.
    Store the real url, and the cut one.
    """
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        """
        Create the url' table.
        """
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS urls(
                            url TEXT,
                            cut TEXT)""")
        self.conn.commit()
        print("URLs table created!")
    
    def add_cut(self, url: str, cut: str):
        """
        Add a user to the database.

        Args:
            url (str): the url
            cut (str): the cut url
        """
        
        self.cursor.execute("INSERT INTO urls VALUES (?, ?)", (url, cut,))
        self.conn.commit()
    
    def get_url(self, cut: str) -> dict:
        """
        Search for a user in the database by name or by email.

        Args:
            cut (str): the user's name

        Returns:
            dict: the url or None if not found.
        """
        
        self.cursor.execute("SELECT * FROM urls WHERE cut=?", (cut,))
        return self.cursor.fetchone()
