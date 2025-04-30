import sqlite3
  
def search_email(email):
    conn = sqlite3.connect('database/leaked_credentials.db')
    c = conn.cursor()
    c.execute("SELECT type, value, source FROM credentials WHERE value = ?", (email,))
    results = c.fetchall()
    conn.close()
    return results
