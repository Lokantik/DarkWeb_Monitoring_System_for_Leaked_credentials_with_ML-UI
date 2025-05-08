import sqlite3

DB_path = r"C:\Users\lokan\Desktop\Dark_Web_Monitoring_System_for_Leaked_Credentials_with-ML&UI\database\leaked_credential.db" 

def create_user(email, password_hash):
    try:
        conn = sqlite3.connect(DB_path)
        c = conn.cursor()
        c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user_by_email(email):
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_path)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user
