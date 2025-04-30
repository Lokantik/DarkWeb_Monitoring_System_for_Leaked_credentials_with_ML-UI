import sqlite3
   
def init_db():
    conn = sqlite3.connect('database/leaked_credentials.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    value TEXT,
                    source TEXT
                )''')
    conn.commit()
    conn.close()
    